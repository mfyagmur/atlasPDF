class InvalidFileTypeError(Exception):
    """Yüklenen dosya gerçek bir PDF değil."""


class FileTooLargeError(Exception):
    """Toplam yükleme boyutu izin verilen limiti aşıyor."""
