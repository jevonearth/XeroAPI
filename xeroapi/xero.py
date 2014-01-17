from client import Client
from resources import XOrganization
from resources import XAccount
from resources import XAccountType
from resources import XBrandingTheme
from resources import XTaxRate
from xeroapi import __version__
import sys

def run_main (token, secret, pem_filepath):
    print "XERO API Version %s" % __version__
    xero_client = Client(token, secret, pem_filepath)
    print XOrganization.get(xero_client)
    #count = 1
    # for account in XAccount.get(xero_client):
    #     print "%03d (%21s) %s" % (count, XAccountType.humanize(account.type), account)
    #     count += 1

    print ",-----------------------------------------------------------------------------------------"
    print "| Branding Themes: "
    print "| ----------------------------------------------------------------------------------------"
    for theme in XBrandingTheme.get(xero_client):
        print "| %s %-22s %2s %s" % (theme.BrandingThemeID,
                                 theme.CreatedDateUTC,
                                 theme.SortOrder,
                                 theme.Name)
    print "`-----------------------------------------------------------------------------------------"
    print "| Tax Rates: "
    print "| ----------------------------------------------------------------------------------------"
    for rate in XTaxRate.get(xero_client):
        print "| %-12s %-32s %8s %8s" % (rate.TaxType,
                                         rate.Name,
                                         rate.DisplayTaxRate,
                                         rate.EffectiveRate)
    print "`-----------------------------------------------------------------------------------------"


if __name__ == "__main__":
    run_main(sys.argv[1], sys.argv[2], sys.argv[3])
