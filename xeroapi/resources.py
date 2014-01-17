from decimal import Decimal
import datetime
import json as simplejson
import xml2json

_DATE_FORMAT = "%Y-%m-%d"

class XEntity(dict):
    """
    Provides an abstract class for the `X` based XERO API Resources.
    """

    def to_xml(self):
        raise NotImplementedError

    @staticmethod
    def xget(client):
        raise NotImplementedError

    @staticmethod
    def xput(client, object):
        raise NotImplementedError

class XOrganization:
    """
    Defines a XERO Organization.
    """
    def __init__(self, name, legalName, paysTax, version, organizationType, baseCurrency):
        self.name = name
        self.legalName = legalName
        self.paysTax = paysTax
        self.version = version
        self.organizationType = organizationType
        self.baseCurrency = baseCurrency

    def __repr__(self):
        """
        Provides a string representation of the XOrganization instance.
        """
        return self.legalName

    @staticmethod
    def get(client):
        """
        Returns the organization instance for the client.
        """
        # Attempt to retrieve the response as a Python dict:
        response = client.get("Organisation")

        # Retrieve the organization:
        retval = XOrganization(response["Response"]["Organisations"]["Organisation"]["Name"],
                               response["Response"]["Organisations"]["Organisation"]["LegalName"],
                               response["Response"]["Organisations"]["Organisation"]["PaysTax"],
                               response["Response"]["Organisations"]["Organisation"]["Version"],
                               response["Response"]["Organisations"]["Organisation"]["OrganisationType"],
                               response["Response"]["Organisations"]["Organisation"]["BaseCurrency"])
        # Done, return:
        return retval

class XAccountType:
    BANK = "BANK"
    CURRENT = "CURRENT"
    CURRLIAB = "CURRLIAB"
    DEPRECIATN = "DEPRECIATN"
    DIRECTCOSTS = "DIRECTCOSTS"
    EQUITY = "EQUITY"
    EXPENSE = "EXPENSE"
    FIXED = "FIXED"
    LIABILITY = "LIABILITY"
    NONCURRENT = "NONCURRENT"
    OTHERINCOME = "OTHERINCOME"
    OVERHEADS = "OVERHEADS"
    PREPAYMENT = "PREPAYMENT"
    REVENUE = "REVENUE"
    SALES = "SALES"
    TERMLIAB = "TERMLIAB"

    @staticmethod
    def humanize(atype):
        """
        Provides a human readable format for the account type.
        """
        transdict = {XAccountType.BANK : "Bank",
                     XAccountType.CURRENT : "Current Asset",
                     XAccountType.CURRLIAB : "Current Liability",
                     XAccountType.DEPRECIATN : "Depreciation",
                     XAccountType.DIRECTCOSTS : "Direct Costs",
                     XAccountType.EQUITY : "Equity",
                     XAccountType.EXPENSE : "Expense",
                     XAccountType.FIXED : "Fixed Asset",
                     XAccountType.LIABILITY : "Liability",
                     XAccountType.NONCURRENT : "Non-Current Asset",
                     XAccountType.OTHERINCOME : "Other Income",
                     XAccountType.OVERHEADS : "Overheads",
                     XAccountType.PREPAYMENT : "Pre-payment",
                     XAccountType.REVENUE : "Revenue",
                     XAccountType.SALES : "Sale",
                     XAccountType.TERMLIAB : "Non-Current Liability"}
        return transdict[atype]

    @staticmethod
    def from_string(atype):
        """
        Translates a string represented type to enum.
        """
        transdict = {"BANK" : XAccountType.BANK,
                     "CURRENT" : XAccountType.CURRENT,
                     "CURRLIAB" : XAccountType.CURRLIAB,
                     "DEPRECIATN" : XAccountType.DEPRECIATN,
                     "DIRECTCOSTS" : XAccountType.DIRECTCOSTS,
                     "EQUITY" : XAccountType.EQUITY,
                     "EXPENSE" : XAccountType.EXPENSE,
                     "FIXED" : XAccountType.FIXED,
                     "LIABILITY" : XAccountType.LIABILITY,
                     "NONCURRENT" : XAccountType.NONCURRENT,
                     "OTHERINCOME" : XAccountType.OTHERINCOME,
                     "OVERHEADS" : XAccountType.OVERHEADS,
                     "PREPAYMENT" : XAccountType.PREPAYMENT,
                     "REVENUE" : XAccountType.REVENUE,
                     "SALES" : XAccountType.SALES,
                     "TERMLIAB" : XAccountType.TERMLIAB}
        return transdict[atype]

class XAccount:
    """
    Defines a XERO Account.
    """

    def __init__(self, id, code, name, type, tax_type, description, system_account, enable_payments):
        self.id = id
        self.code = code
        self.name = name
        self.type = type
        self.tax_type = tax_type
        self.description = description
        self.system_account = system_account
        self.enable_payments = enable_payments

    def __repr__(self):
        """
        Provides a string representation of the XOrganization instance.
        """
        return "[%s] %s" % (self.code, self.name)

    @staticmethod
    def get(client):
        """
        Returns account instance(s) for the client.
        """
        # Attempt to retrieve the response as a Python dict:
        response = client.get("Account")

        # Iterate over the accounts:
        retval = []
        for daccount in response["Response"]["Accounts"]["Account"]:
            account = XAccount(daccount["AccountID"],
                               daccount["Code"],
                               daccount["Name"],
                               XAccountType.from_string(daccount["Type"]),
                               daccount["TaxType"],
                               daccount["Description"] if daccount.has_key("Description") else None,
                               daccount["SystemAccount"] if daccount.has_key("SystemAccount") else None,
                               daccount["EnablePaymentsToAccount"] == "true")
            retval.append(account)

        # Done, return:
        return retval

class XItem(XEntity):
    """
    Provides an Item class which is compatible with XERO API.
    """

    def __init__(self):
        """
        Constructs a new :class:`XItem` model instance.
        """
        pass

    def get_code(self):
        """
        Returns the code.
        """
        return self["Code"]

    def set_code(self, code):
        """
        Sets the code.
        """
        self["Code"] = code

    Code = property(get_code, set_code)

    def get_description(self):
        """
        Returns the description.
        """
        return self["Description"]

    def set_description(self, description):
        """
        Sets the description.
        """
        self["Description"] = description

    Description = property(get_description, set_description)


    def get_purchase_details(self):
        """
        Returns the purchase details.
        """
        return self.get("PurchaseDetails")

    def set_purchase_details(self, purchase_details):
        """
        Sets the purchase details.

        TODO: Provide a more generalized representation.
        #   <PurchaseDetails>
        #     <UnitPrice>42.00</UnitPrice>
        #     <AccountCode>300</AccountCode>
        #     <TaxType>NONE</TaxType>
        #   </PurchaseDetails>
        """
        self["PurchaseDetails"] = purchase_details

    PurchaseDetails = property(get_purchase_details, set_purchase_details)


    def get_sales_details(self):
        """
        Returns the sales details.
        """
        return self.get("SalesDetails")

    def set_sales_details(self, sales_details):
        """
        Sets the sales details.

        TODO: Provide a more generalized representation.
        #   <SalesDetails>
        #     <UnitPrice>42.00</UnitPrice>
        #     <AccountCode>300</AccountCode>
        #     <TaxType>NONE</TaxType>
        #   </SalesDetails>
        """
        self["SalesDetails"] = sales_details

    SalesDetails = property(get_sales_details, set_sales_details)


    def to_xml(self):
        """
        Provides a json representation of the invoice.
        """
        return xml2json.json2xml(simplejson.dumps({"Item": self}))

    # @staticmethod
    # def get(client):
    #     """
    #     Returns XItem instances.
    #     """
    #     # Attempt to retrieve the response as a Python dict:
    #     response = client.get("Item")

    #     # Iterate over the accounts:
    #     retval = []

    #     if not response["Response"].has_key("Items"):
    #         return retval

    #     for item in response["Response"]["Items"]["Item"]:
    #         print item
    #         account = XItem(item["Code"],
    #                         item["Description"],
    #                         item["PurchaseDetails"]["UnitPrice"] if item.has_key("PurchaseDetails") else None,
    #                         item["PurchaseDetails"]["AccountCode"] if item.has_key("PurchaseDetails") else None,
    #                         item["SalesDetails"]["UnitPrice"] if item.has_key("SalesDetails") else None,
    #                         item["SalesDetails"]["AccountCode"] if item.has_key("SalesDetails") else None)
    #         retval.append(account)

    #     # Done, return:
    #     return retval

    @staticmethod
    def post(client, item):
        """
        Creates a new item on the XERO.
        """
        # Post the item:
        response = client.post("Item", item.to_xml())

        # Done, return the xitem:
        return response["Response"]

class XContact(XEntity):
    """
    Provides a contact class which is compatible with XERO API.
    """

    class Status:
        ACTIVE = "ACTIVE"
        ACCREC = "DELETED"

        @classmethod
        def get_all_types(cls):
            return [cls.ACTIVE, cls.DELETED]

    def __init__(self, status=Status.ACTIVE):
        """
        Constructs a new :class:`XContact` model instance.
        """
        self.Status = status

    def get_contact_id(self):
        """
        Returns the contact id.
        """
        return self.get("ContactID")

    def set_contact_id(self, contact_id):
        """
        Sets the contact id.
        """
        self["ContactID"] = contact_id

    ContactID = property(get_contact_id, set_contact_id)

    def get_contact_number(self):
        """
        Returns the contact number.
        """
        return self.get("ContactNumber")

    def set_contact_number(self, contact_number):
        """
        Sets the contact number.
        """
        self["ContactNumber"] = contact_number

    ContactNumber = property(get_contact_number, set_contact_number)

    def get_name(self):
        """
        Returns the name.
        """
        return self.get("Name")

    def set_name(self, name):
        """
        Sets the name.
        """
        self["Name"] = name

    Name = property(get_name, set_name)

    def get_contact_status(self):
        """
        Returns the contact status.
        """
        return self.get("ContactStatus")

    def set_contact_status(self, contact_status):
        """
        Sets the contact status.
        """
        if contact_status in self.__class__.ContactStatus.get_all_types():
            self["ContactStatus"] = contactstatus
        else:
            raise ValueError("ContactStatus is unknown: %s" % contact_status)

    ContactStatus = property(get_contact_status, set_contact_status)

    def get_email_address(self):
        """
        Returns the email address.
        """
        return self.get("EmailAddress")

    def set_email_address(self, email_address):
        """
        Sets the email_address.
        """
        self["EmailAddress"] = email_address

    EmailAddress = property(get_email_address, set_email_address)

    def get_skype_user_name(self):
        """
        Returns the Skype user name.
        """
        return self.get("SkypeUserName")

    def set_skype_user_name(self, skype_user_name):
        """
        Sets the Skype user name.
        """
        self["SkypeUserName"] = skype_user_name

    SkypeUserName = property(get_skype_user_name, set_skype_user_name)

    def get_bank_account_details(self):
        """
        Returns the bank account details.
        """
        return self.get("BankAccountDetails")

    def set_bank_account_details(self, bank_account_details):
        """
        Sets the bank account details.
        """
        self["BankAccountDetails"] = bank_account_details

    BankAccountDetails = property(get_bank_account_details, set_bank_account_details)

    def get_tax_number(self):
        """
        Returns the tax number.
        """
        return self.get("TaxNumber")

    def set_tax_number(self, tax_number):
        """
        Sets the tax number.
        """
        self["TaxNumber"] = tax_number

    TaxNumber = property(get_tax_number, set_tax_number)

    def get_first_name(self):
        """
        Returns the first name.
        """
        return self.get("FirstName")

    def set_first_name(self, first_name):
        """
        Sets the first name.
        """
        self["FirstName"] = first_name

    FirstName = property(get_first_name, set_first_name)

    def get_last_name(self):
        """
        Returns the last name.
        """
        return self.get("LastName")

    def set_last_name(self, last_name):
        """
        Sets the last name.
        """
        self["LastName"] = last_name

    LastName = property(get_last_name, set_last_name)

    def get_default_currency(self):
        """
        Returns the default currency.
        """
        return self.get("DefaultCurrency")

    def set_default_currency(self, default_currency):
        """
        Sets the default currency.
        """
        self["DefaultCurrency"] = default_currency

    DefaultCurrency = property(get_default_currency, set_default_currency)

    def get_addresses(self):
        """
        Returns the addresses.
        """
        return self.get("Addresses")

    def set_addresses(self, addresses):
        """
        Sets the addresses.

        TODO: Provide more addresses.
        """
        _address = dict()
        _address["AddressType"] = "POBOX"
        _address["AddressLine1"] = addresses["AddressLine1"]
        _address["AddressLine2"] = addresses["AddressLine2"]
        _address["AddressLine3"] = addresses["AddressLine3"]
        _address["AddressLine4"] = addresses["AddressLine4"]
        _address["City"] = addresses["City"]
        _address["Region"] = addresses["Region"]
        _address["PostalCode"] = addresses["PostalCode"]
        _address["Country"] = addresses["Country"]
        self["Addresses"] = dict(Address=_address)

    Addresses = property(get_addresses, set_addresses)

    def get_phones(self):
        """
        Returns the phones.
        """
        return self.get("Phones")

    def set_phones(self, phones):
        """
        Sets the phones.

        TODO: Provide more phones.
        """
        _phone = dict()
        _phone["PhoneType"] = "DEFAULT"
        _phone["PhoneNumber"] = phones
        self["Phones"] = dict(Phone=_phone)

    Phones = property(get_phones, set_phones)

    def to_xml(self):
        """
        Provides a json representation of the contact.
        """
        return xml2json.json2xml(simplejson.dumps({"Contact": self}))


class XInvoice(XEntity):
    """
    Provides an invoice class which is compatible with XERO API.
    """

    class InvoiceType:
        ACCPAY = "ACCPAY"
        ACCREC = "ACCREC"

        @classmethod
        def get_all_types(cls):
            return [cls.ACCREC, cls.ACCPAY]

    class InvoiceLineAmountType:
        Exclusive = "Exclusive"
        Inclusive = "Inclusive"
        NoTax = "NoTax"

        @classmethod
        def get_all_types(cls):
            return [cls.Exclusive, cls.Inclusive, cls.NoTax]

    class InvoiceStatus:
        DRAFT = "DRAFT"
        SUBMITTED = "SUBMITTED"
        DELETED = "DELETED"
        AUTHORISED = "AUTHORISED"
        PAID = "PAID"
        VOIDED = "VOIDED"

        @classmethod
        def get_all_types(cls):
            return [cls.DRAFT,
                    cls.SUBMITTED,
                    cls.DELETED,
                    cls.AUTHORISED,
                    cls.PAID,
                    cls.VOIDED]

    def __init__(self,
                 ctype=InvoiceType.ACCREC,
                 status=InvoiceStatus.DRAFT,
                 line_amount_types=InvoiceLineAmountType.Exclusive):
        """
        Constructs a new :class:`XInvoice` model instance.
        """
        self.Type = ctype
        self.Status = status
        self.LineAmountTypes = line_amount_types

    def get_type(self):
        """
        Returns the type.
        """
        return self.get("Type")

    def set_type(self, ctype):
        """
        Sets the type.
        """
        if ctype in self.__class__.InvoiceType.get_all_types():
            self["Type"] = ctype
        else:
            raise ValueError("Unknown invoice type: %s" % ctype)

    Type = property(get_type, set_type)

    def get_contact(self):
        """
        Returns the contact of the customer.
        """
        return self.get("Contact")

    def set_contact(self, contact):
        """
        Sets the contact information of the customer.
        """
        if not isinstance(contact, XContact):
            raise ValueError("Contact should be of type XContact")
        self["Contact"] = contact

    Contact = property(get_contact, set_contact)

    def get_date(self):
        """
        Returns the invoice date.
        """
        date = self.get("Date")
        if date:
            return datetime.datetime.strptime(date, _DATE_FORMAT)
        else:
            return None

    def set_date(self, date):
        """
        Sets the invoice date.
        """
        if not isinstance(date, datetime.datetime):
            raise ValueError("Date should be of datetime.datetime type")
        self["Date"] = date.strftime(_DATE_FORMAT)

    Date = property(get_date, set_date)

    def get_due_date(self):
        """
        Returns the invoice due date.
        """
        date = self.get("DueDate")
        if date:
            return datetime.datetime.strptime(date, _DATE_FORMAT)
        else:
            return None

    def set_due_date(self, date):
        """
        Sets the invoice due date.
        """
        if not isinstance(date, datetime.datetime):
            raise ValueError("Date should be of datetime.datetime type")
        self["DueDate"] = date.strftime(_DATE_FORMAT)

    DueDate = property(get_due_date, set_due_date)

    def get_invoice_number(self):
        """
        Returns the invoice number.
        """
        return self.get("InvoiceNumber")

    def set_invoice_number(self, invoice_number):
        """
        Sets the invoice number.
        """
        self["InvoiceNumber"] = invoice_number

    InvoiceNumber = property(get_invoice_number, set_invoice_number)

    def get_reference(self):
        """
        Returns the invoice number.
        """
        return self.get("Reference")

    def set_reference(self, reference):
        """
        Sets the invoice number.
        """
        self["Reference"] = reference

    Reference = property(get_reference, set_reference)

    def get_branding(self):
        """
        Returns the branding theme identifier.
        """
        return self.get("BrandingThemeID")

    def set_branding(self, branding):
        """
        Sets the branding theme identifier.
        """
        self["BrandingThemeID"] = branding

    BrandingThemeID = property(get_branding, set_branding)

    def get_url(self):
        """
        Returns the url.
        """
        return self.get("Url")

    def set_url(self, url):
        """
        Sets the url.

        TODO: Type check may be needed
        """
        self["Url"] = url

    Url = property(get_url, set_url)

    def get_currency_code(self):
        """
        Returns the currency code.
        """
        return self.get("CurrencyCode")

    def set_currency_code(self, currency_code):
        """
        Sets the currency code.

        TODO: Need to check against XERO provided codes.
        """
        if len(currency_code) != 3:
            raise ValueError("Currency code should be three letters")
        self["CurrencyCode"] = currency_code

    CurrencyCode = property(get_currency_code, set_currency_code)

    def get_status(self):
        """
        Returns the status.
        """
        return self.get("Status")

    def set_status(self, status):
        """
        Sets the status.
        """
        if status in self.__class__.InvoiceStatus.get_all_types():
            self["Status"] = status
        else:
            raise ValueError("Status is unknown: %s" % status)

    Status = property(get_status, set_status)

    def get_line_amount_types(self):
        """
        Returns the line amount types.
        """
        return self.get("LineAmountTypes")

    def set_line_amount_types(self, line_amount_types):
        """
        Sets the line amount types.
        """
        if line_amount_types in self.__class__.InvoiceLineAmountType.get_all_types():
            self["LineAmountTypes"] = line_amount_types
        else:
            raise ValueError("LineAmountType is unknown: %s" % line_amount_types)

    LineAmountTypes = property(get_line_amount_types, set_line_amount_types)

    def get_sub_total(self):
        """
        Returns the sub total.
        """
        sub_total = self.get("SubTotal")
        if sub_total:
            return Decimal(sub_total)
        else:
            return None

    def set_sub_total(self, sub_total):
        """
        Sets the sub total. All inputs are quantized to 0.00 form.
        """
        if not isinstance(sub_total, Decimal):
            raise ValueError("SubTotal should be of type Decimal")
        self["SubTotal"] = str(sub_total.quantize(Decimal("0.00")))

    SubTotal = property(get_sub_total, set_sub_total)

    def get_total_tax(self):
        """
        Returns the total tax.
        """
        total_tax = self.get("TotalTax")
        if total_tax:
            return Decimal(total_tax)
        else:
            return None

    def set_total_tax(self, total_tax):
        """
        Sets the total tax. All inputs are quantized to 0.00 form.
        """
        if not isinstance(total_tax, Decimal):
            raise ValueError("TotalTax should be of type Decimal")
        self["TotalTax"] = str(total_tax.quantize(Decimal("0.00")))

    TotalTax = property(get_total_tax, set_total_tax)

    def get_total(self):
        """
        Returns the total amount.
        """
        total = self.get("Total")
        if total:
            return Decimal(total)
        else:
            return None

    def set_total(self, total):
        """
        Sets the total amount. All inputs are quantized to 0.00 form.
        """
        if not isinstance(total, Decimal):
            raise ValueError("Total should be of type Decimal")
        self["Total"] = str(total.quantize(Decimal("0.00")))

    Total = property(get_total, set_total)

    def get_line_items(self):
        """
        Returns the invoice line items.
        """
        if self.get("LineItems"):
            return self.get("LineItems").get("LineItem")
        else:
            return None

    def set_line_items(self, line_items):
        """
        Sets the invoice lines.

        TODO: Provide a more generalized representation.
        # <Description>Red Sweater</Description>
        # <Quantity>5</Quantity>
        # <AccountCode>200</AccountCode>
        # <ItemCode>2010-SWEATER-RED</ItemCode>
        """
        self["LineItems"] = {"LineItem": line_items}

    LineItems = property(get_line_items, set_line_items)

    def to_xml(self):
        """
        Provides a json representation of the invoice.
        """
        return xml2json.json2xml(simplejson.dumps({"Invoice": self}))

    @staticmethod
    def xget(client):
        """
        Returns XItem instances.
        """
        # Attempt to retrieve the response as a Python dict:
        response = client.get("Invoice")

        # Iterate over the accounts:
        retval = []

        if not response["Response"].has_key("Invoices"):
            return retval

        #for item in response["Response"]["Invoices"]["Invoice"]:
            #print item
            # account = XItem(item["Code"],
            #                 item["Description"],
            #                 item["PurchaseDetails"]["UnitPrice"] if item.has_key("PurchaseDetails") else None,
            #                 item["PurchaseDetails"]["AccountCode"] if item.has_key("PurchaseDetails") else None,
            #                 item["SalesDetails"]["UnitPrice"] if item.has_key("SalesDetails") else None,
            #                 item["SalesDetails"]["AccountCode"] if item.has_key("SalesDetails") else None)
            # retval.append(account)

        # Done, return:
        return retval

    @staticmethod
    def xpost(client, invoice):
        """
        Updates or Creates a new invoice on the XERO.
        """
        # Post the item:
        response = client.post("Invoice", invoice.to_xml())

        return response["Response"]


class XBrandingTheme(XEntity):
    """
    Provides a branding theme class which is compatible with XERO API.
    """

    def __init__(self, response):
        """
        Constructs a new :class:`XBrandingTheme` model instance.
        """
        self._response = response

    @property
    def BrandingThemeID(self):
        """
        Returns the branding theme id.
        """
        return self._response["BrandingThemeID"]

    @property
    def Name(self):
        """
        Returns the name.
        """
        return self._response["Name"]

    @property
    def SortOrder(self):
        """
        Returns the order.
        """
        return self._response["SortOrder"]

    @property
    def CreatedDateUTC(self):
        """
        Returns the creation date.
        """
        return self._response["CreatedDateUTC"]

    @staticmethod
    def get(client):
        """
        Returns XBrandingTheme instances.
        """
        # Attempt to retrieve the response as a Python dict:
        response = client.get("BrandingTheme")

        # Iterate over the accounts:
        retval = []

        # If no theme, return []
        if not response["Response"].has_key("BrandingThemes"):
            return retval

        # If only one instance is returned, xml2json returns
        # dictionary. Put the single item back into a list.
        if isinstance(response["Response"]["BrandingThemes"]["BrandingTheme"], dict):
            response["Response"]["BrandingThemes"]["BrandingTheme"] = [response["Response"]["BrandingThemes"]["BrandingTheme"]]

        # Iterate over the values:
        for item in response["Response"]["BrandingThemes"]["BrandingTheme"]:
            retval.append(XBrandingTheme(item))

        # Done, return:
        return retval


class XTaxRate(XEntity):
    """
    Provides a tax rate class which is compatible with XERO API.
    """

    def __init__(self, response):
        """
        Constructs a new :class:`XTaxRate` model instance.
        """
        self._response = response

    @property
    def TaxType(self):
        """
        Returns tax type.
        """
        return self._response["TaxType"]

    @property
    def Name(self):
        """
        Returns the name.
        """
        return self._response["Name"]

    @property
    def DisplayTaxRate(self):
        """
        Returns display tax rate.
        """
        return self._response["DisplayTaxRate"]

    @property
    def EffectiveRate(self):
        """
        Returns effective tax rate.
        """
        return self._response.get("EffectiveTaxRate")

    @staticmethod
    def get(client):
        """
        Returns XBrandingTheme instances.
        """
        # Attempt to retrieve the response as a Python dict:
        response = client.get("TaxRate")

        # Declare the return value:
        retval = []

        # If no rates, return []
        if not response["Response"].has_key("TaxRates"):
            return retval

        # If only one instance is returned, xml2json returns
        # dictionary. Put the single item back into a list.
        if isinstance(response["Response"]["TaxRates"]["TaxRate"], dict):
            response["Response"]["TaxRates"]["TaxRate"] = [response["Response"]["TaxRates"]["TaxRate"]]

        # Iterate over the values:
        for item in response["Response"]["TaxRates"]["TaxRate"]:
            retval.append(XTaxRate(item))

        # Done, return:
        return retval

