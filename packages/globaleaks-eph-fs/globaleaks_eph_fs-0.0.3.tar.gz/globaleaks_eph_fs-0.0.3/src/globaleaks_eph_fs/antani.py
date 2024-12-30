import argparse
import errno
import os
import stat
import uuid
import logging
from fuse import FUSE, FuseOSError, Operations
from tempfile import mkdtemp

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import ChaCha20

# Configure logging to log only in the command line
logging.basicConfig(
    level=logging.DEBUG,  # Log all events
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class EphemeralFile:
    def __init__(self, filesdir):
        """
        Initialize ChaCha20 encryption with a randomly generated key and nonce.
        """
        self.fd = None
        self.filename = str(uuid.uuid4())
        self.filepath = os.path.join(filesdir, self.filename)
        self.nonce = os.urandom(16)  # 128-bit nonce
        self.key = os.urandom(32)    # 256-bit key
        self.cipher = Cipher(ChaCha20(self.key, self.nonce), mode=None)
        self.size = 0
        self.enc = self.cipher.encryptor()
        self.dec = None

    def open(self, mode):
        """
        Open the file for read or write operations.
        """
        if mode == 'w':
            self.fd = os.open(self.filepath, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
            self.dec = None
        else:
            self.fd = os.open(self.filepath, os.O_RDONLY)
            self.dec = self.cipher.decryptor()
        return self

    def write(self, data):
        """
        Write encrypted data to the file.
        """
        if isinstance(data, str):
            data = data.encode('utf-8')

        encrypted_data = self.enc.update(data)
        os.write(self.fd, encrypted_data)
        self.size += len(data)

    def read(self, size, offset):
        """
        Read and decrypt data from the file with random access support.
        """
        if self.dec is None:
            # Initialize decryption on first read
            self.dec = self.cipher.decryptor()

        # Reinitialize the decryption context for random access
        temp_cipher = Cipher(ChaCha20(self.key, self.nonce), mode=None)
        temp_dec = temp_cipher.decryptor()

        # Seek to the correct offset by discarding decrypted bytes
        os.lseek(self.fd, 0, os.SEEK_SET)  # Reset file pointer to the start
        discard_size = offset
        chunk_size = 4096  # Read in chunks to avoid memory overhead

        while discard_size > 0:
            to_read = min(discard_size, chunk_size)
            temp_dec.update(os.read(self.fd, to_read))
            discard_size -= to_read

        # Now read and decrypt the requested amount of data
        data = temp_dec.update(os.read(self.fd, size))
        return data

    def close(self):
        """
        Close the file descriptor.
        """
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def truncate(self, length):
        if self.fd is None:
            # Open the file in write mode if not already open
            self.open('w')
        os.ftruncate(self.fd, length)
        self.size = length

    def __del__(self):
        """
        Ensure proper cleanup by closing and deleting the file.
        """
        self.close()
        try:
            os.remove(self.filepath)
        except FileNotFoundError:
            pass


class EphemeralOperations(Operations):
    def __init__(self, storage_directory=None):
        if storage_directory is None:
            storage_directory = mkdtemp()

        self.storage_directory = storage_directory
        self.files = {}
        self.default_permissions = 0o660
        self.uid = os.getuid()
        self.gid = os.getgid()

    def getattr(self, path, fh=None):
        logging.debug(f"getattr called on path: {path}")
        if path == '/':
            st = {'st_mode': (stat.S_IFDIR | 0o750), 'st_nlink': 2}
        else:
            file = self.files.get(path)
            if file is None or not os.path.exists(file.filepath):
                raise OSError(errno.ENOENT, "No such file or directory", path)
            file_stat = os.stat(file.filepath)
            st = {
                'st_mode': (stat.S_IFREG | 0o660),
                'st_size': file.size,
                'st_nlink': 1,
                'st_uid': self.uid,
                'st_gid': self.gid,
                'st_atime': file_stat.st_atime,
                'st_mtime': file_stat.st_mtime,
                'st_ctime': file_stat.st_ctime,
            }
        return st

    def readdir(self, path, fh):
        logging.debug(f"readdir called on path: {path}")
        return ['.', '..'] + [os.path.basename(f) for f in self.files]

    def create(self, path, mode):
        logging.info(f"create called on path: {path} with mode: {oct(mode)}")
        file = EphemeralFile(self.storage_directory)
        file.open('w')
        os.chmod(file.filepath, self.default_permissions)
        os.chown(file.filepath, self.uid, self.gid)
        self.files[path] = file
        return file.fd

    def open(self, path, flags):
        logging.info(f"open called on path: {path} with flags: {flags}")
        file = self.files.get(path)
        if file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        mode = 'w' if (flags & os.O_RDWR or flags & os.O_WRONLY) else 'r'
        file.open(mode)
        return file.fd

    def read(self, path, size, offset, fh):
        """
        Read data from the file at the given offset.
        """
        logging.debug(f"read called on path: {path}, size: {size}, offset: {offset}")
        file = self.files.get(path)
        if file is None:
            raise FuseOSError(errno.ENOENT)
        return file.read(size, offset)

    def write(self, path, data, offset, fh):
        logging.debug(f"write called on path: {path}, size: {len(data)}, offset: {offset}")
        file = self.files.get(path)
        file.write(data)
        return len(data)

    def unlink(self, path):
        logging.info(f"unlink called on path: {path}")
        file = self.files.pop(path, None)
        if file:
            file.close()
            os.remove(file.filepath)

    def release(self, path, fh):
        logging.info(f"release called on path: {path}")
        file = self.files.get(path)
        if file:
            file.close()

    def truncate(self, path, length):
        file = self.files.get(path)
        if file is None:
            raise OSError(errno.ENOENT, "No such file or directory", path)
        file.truncate(length)

    def chmod(self, path, mode):
        logging.warning(f"chmod called on {path} with mode {oct(mode)}, but not supported.")
        raise OSError(errno.ENOSYS, "Operation not supported")

    def getxattr(self, path, name, position=0):
        """
        Get extended attributes. Return ENOATTR for unsupported attributes.
        """
        logging.info(f"getxattr called on {path} for attribute {name}")
        # Return an empty attribute or raise ENOATTR for unsupported attributes
        raise FuseOSError(errno.ENODATA)  # No such attribute


    def listxattr(self, path):
        """
        List extended attributes. Return an empty list.
        """
        logging.info(f"listxattr called on {path}")
        return []  # No extended attributes are supported


class EphemeralFS(FUSE):
    def __init__(self, mount_point, storage_directory=None, **fuse_args):
        self.mount_point = mount_point
        self.storage_directory = storage_directory

        os.makedirs(self.mount_point, exist_ok=True)
        if self.storage_directory:
            os.makedirs(self.storage_directory, exist_ok=True)

        super().__init__(EphemeralOperations(self.storage_directory), self.mount_point, **fuse_args)


def main():
    parser = argparse.ArgumentParser(description="GLOBALEAKS EPHEMERAL FS")
    parser.add_argument('mount_point', help="Path to mount the filesystem")
    parser.add_argument('--storage_directory', '-s', help="Optional storage directory. Defaults to a temporary directory.")
    args = parser.parse_args()

    logging.info("Starting EphemeralFS...")
    EphemeralFS(args.mount_point, args.storage_directory, nothreads=True, foreground=True)


if __name__ == '__main__':
    main()
