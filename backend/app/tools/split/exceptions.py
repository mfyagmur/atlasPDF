class InvalidPDFError(Exception):
    """PDF bozuk, şifreli veya okunamıyor."""


class InvalidPageRangeError(Exception):
    """Sayfa aralığı formatı geçersiz veya toplam sayfa sayısını aşıyor."""
