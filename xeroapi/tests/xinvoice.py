from decimal import Decimal
from xeroapi.resources import XInvoice
from xeroapi.resources import XContact
import datetime
import unittest

__all__ = ["XInvoiceARTest"]

class XInvoiceARTest(unittest.TestCase):
    """
    Provides a Accounts Receivable invoice test suit.
    """

    def setUp(self):
        self.invoice = XInvoice()

    def test_construction(self):
        """
        Tests the constructor.
        """
        self.assertEqual(self.invoice.Type, XInvoice.InvoiceType.ACCREC)
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.DRAFT)

    def test_slot_Type(self):
        """
        Tests the Type slot of the invoice.
        """
        self.assertRaises(ValueError, self.invoice.set_type, "BLABLA")
        self.assertRaises(NotImplementedError,
                          self.invoice.set_type,
                          XInvoice.InvoiceType.ACCPAY)
        self.invoice.Type = XInvoice.InvoiceType.ACCREC
        self.assertEqual(self.invoice.Type, XInvoice.InvoiceType.ACCREC)

    def test_slot_Contact(self):
        """
        Tests the Contact slot of the invoice.
        """
        self.assertEqual(self.invoice.Contact, None)
        self.assertRaises(ValueError, self.invoice.set_type, "BLABLA")
        contact = XContact()
        contact.ContactNumber = "CARI-00001"
        contact.Name = "TEST CONTACT NAME"
        contact.Addresses = {"AddressLine1": "Address Line 1",
                             "AddressLine2": "Address Line 2",
                             "AddressLine3": "Address Line 3",
                             "AddressLine4": "Address Line 4",
                             "City": "City",
                             "Region": "Region",
                             "PostalCode": "PostalCode",
                             "Country": "Country"}
        self.invoice.Contact = contact
        self.invoice.Phones = "11235813"
        self.assertEqual(str(self.invoice.Contact), str(contact))

    def test_slot_Date(self):
        """
        Tests the Date slot of the invoice.
        """
        self.assertEqual(self.invoice.Date, None)
        self.invoice.Date = datetime.datetime(2011, 04, 01)
        self.assertEqual(self.invoice.Date, datetime.datetime(2011, 04, 01))
        self.assertEqual(self.invoice["Date"], "04/01/2011")
        self.assertRaises(ValueError, self.invoice.set_date, "04/01/2011")

    def test_slot_DueDate(self):
        """
        Tests the DueDate slot of the invoice.
        """
        self.assertEqual(self.invoice.DueDate, None)
        self.invoice.DueDate = datetime.datetime(2011, 05, 01)
        self.assertEqual(self.invoice.DueDate, datetime.datetime(2011, 05, 01))
        self.assertEqual(self.invoice["DueDate"], "05/01/2011")
        self.assertRaises(ValueError, self.invoice.set_date, "05/01/2011")

    def test_slot_InvoiceNumber(self):
        """
        Tests the InvoiceNumber slot of the invoice.
        """
        self.assertEqual(self.invoice.InvoiceNumber, None)
        self.invoice.InvoiceNumber = "INV-00001"
        self.assertEqual(self.invoice.InvoiceNumber, "INV-00001")

    def test_slot_Reference(self):
        """
        Tests the Reference slot of the invoice.
        """
        self.assertEqual(self.invoice.Reference, None)
        self.invoice.Reference = "REF-00001"
        self.assertEqual(self.invoice.Reference, "REF-00001")

    def test_slot_BrandingThemeID(self):
        """
        Tests the BrandingThemeID slot of the invoice.
        """
        self.assertEqual(self.invoice.BrandingThemeID, None)
        self.invoice.BrandingThemeID = "BTI-00001"
        self.assertEqual(self.invoice.BrandingThemeID, "BTI-00001")

    def test_slot_Url(self):
        """
        Tests the Url slot of the invoice.
        """
        self.assertEqual(self.invoice.Url, None)
        self.invoice.Url = "http://www.beesdom.com"
        self.assertEqual(self.invoice.Url, "http://www.beesdom.com")

    def test_slot_CurrencyCode(self):
        """
        Tests the CurrencyCode slot of the invoice.
        """
        self.assertEqual(self.invoice.CurrencyCode, None)
        self.assertRaises(ValueError, self.invoice.set_currency_code, "XYZA")
        self.assertEqual(self.invoice.CurrencyCode, None)
        self.invoice.CurrencyCode = "NZD"
        self.assertEqual(self.invoice.CurrencyCode, "NZD")

    def test_slot_Status(self):
        """
        Tests the Status slot of the invoice.
        """
        self.assertRaises(ValueError, self.invoice.set_status, "BLABLA")
        self.invoice.Status = XInvoice.InvoiceStatus.SUBMITTED
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.SUBMITTED)
        self.invoice.Status = XInvoice.InvoiceStatus.DELETED
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.DELETED)
        self.invoice.Status = XInvoice.InvoiceStatus.AUTHORISED
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.AUTHORISED)
        self.invoice.Status = XInvoice.InvoiceStatus.PAID
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.PAID)
        self.invoice.Status = XInvoice.InvoiceStatus.VOIDED
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.VOIDED)
        self.invoice.Status = XInvoice.InvoiceStatus.DRAFT
        self.assertEqual(self.invoice.Status, XInvoice.InvoiceStatus.DRAFT)

    def test_slot_LineAmountTypes(self):
        """
        Tests the LineAmountTypes slot of the invoice.
        """
        self.assertRaises(ValueError, self.invoice.set_line_amount_types, "BLABLA")
        self.invoice.LineAmountTypes = XInvoice.InvoiceLineAmountType.Exclusive
        self.assertEqual(self.invoice.LineAmountTypes, XInvoice.InvoiceLineAmountType.Exclusive)
        self.invoice.LineAmountTypes = XInvoice.InvoiceLineAmountType.NoTax
        self.assertEqual(self.invoice.LineAmountTypes, XInvoice.InvoiceLineAmountType.NoTax)
        self.invoice.LineAmountTypes = XInvoice.InvoiceLineAmountType.Inclusive
        self.assertEqual(self.invoice.LineAmountTypes, XInvoice.InvoiceLineAmountType.Inclusive)

    def test_slot_SubTotal(self):
        """
        Tests the SubTotal slot of the invoice.
        """
        self.assertEqual(self.invoice.SubTotal, None)
        self.invoice.SubTotal = Decimal("100.10")
        self.assertEqual(self.invoice.SubTotal, Decimal("100.10"))
        self.assertEqual(self.invoice["SubTotal"], "100.10")
        self.assertRaises(ValueError, self.invoice.set_date, "BLABLA")
        self.invoice.SubTotal = Decimal("100.101")
        self.assertEqual(self.invoice.SubTotal, Decimal("100.10"))
        self.assertEqual(self.invoice["SubTotal"], "100.10")

    def test_slot_TotalTax(self):
        """
        Tests the TotalTax slot of the invoice.
        """
        self.assertEqual(self.invoice.TotalTax, None)
        self.invoice.TotalTax = Decimal("12.10")
        self.assertEqual(self.invoice.TotalTax, Decimal("12.10"))
        self.assertEqual(self.invoice["TotalTax"], "12.10")
        self.assertRaises(ValueError, self.invoice.set_date, "BLABLA")
        self.invoice.TotalTax = Decimal("12.101")
        self.assertEqual(self.invoice.TotalTax, Decimal("12.10"))
        self.assertEqual(self.invoice["TotalTax"], "12.10")

    def test_slot_Total(self):
        """
        Tests the Total slot of the invoice.
        """
        self.assertEqual(self.invoice.Total, None)
        self.invoice.Total = Decimal("112.20")
        self.assertEqual(self.invoice.Total, Decimal("112.20"))
        self.assertEqual(self.invoice["Total"], "112.20")
        self.assertRaises(ValueError, self.invoice.set_date, "BLABLA")
        self.invoice.Total = Decimal("112.201")
        self.assertEqual(self.invoice.Total, Decimal("112.20"))
        self.assertEqual(self.invoice["Total"], "112.20")

    def test_slot_Lines(self):
        """
        Tests the Lines slot of the invoice.
        """
        self.assertEqual(self.invoice.Lines, None)
        lines = [
            {"ItemCode": "ItemCode1",
             "AccountCode": "AccountCode1",
             "Quantity": "Quantity1"},
            {"ItemCode": "ItemCode2",
             "AccountCode": "AccountCode2",
             "Quantity": "Quantity2"}]
        self.invoice.Lines = lines
        self.assertEqual(self.invoice.Lines, lines)
