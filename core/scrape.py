import requests
from lxml import etree


def scrape(html, data):
    tree = etree.HTML(html)

    entry = tree.xpath('//div[@id="shoppingitems"]/div[@class="br"]')
    for row in entry:
        site_number = row.xpath(
            './div[1]/div[@class="siteListLabel"]/a/text()')[0]
        site_loop = row.xpath('./div[2]/text()')[0]
        site_type = row.xpath('./div[3]/text()')[0]
        max_people = row.xpath('./div[4]/text()')[0]
        driveway_length = row.xpath('./div[5]/text()')[0]
        availability = row.xpath('./div[7]//text()')

        data.append({
            "site_number": site_number,
            "site_loop": site_loop,
            "site_type": site_type,
            "max_people": max_people,
            "driveway_length": driveway_length,
            "availability": "not available" not in " ".join(availability).replace("\n", "")
        })

    navbar = tree.xpath(
        '//span[@class="pagenav"]/a[@id="resultNext_top"]/@href')

    if len(navbar) == 0:
        return

    return navbar[0]


def get_data():
    url = "https://pennsylvaniastateparks.reserveamerica.com/camping/promised-land-state-park/r/campgroundDetails.do?contractCode=PA&parkId=880414"

    data = {
        "contractCode": "PA",
        "parkId": "880414",
        "siteTypeFilter": "ALL",
        "lob": "",
        "availStatus": "",
        "submitSiteForm": "true",
        "search": "site",
        "campingDate": "Sat May 24 2025",
        "lengthOfStay": "2",
        "campingDateFlex": "",
        "currentMaximumWindow": "24",
        "contractDefaultMaxWindow": "MS:24,LARC:24,GA:24,SC:13,PA:24,LA:13,TX:5,NY:24,OR:7,CT:11",
        "stateDefaultMaxWindow": "PA:24",
        "defaultMaximumWindow": "12",
        "loop": "881430",
    }

    # Start Session and Get Cache
    session = requests.Session()
    session.get(url)

    # Getting Initial data from first page
    r = session.post(url, data=data)

    hold = []
    next = scrape(r.text, hold)

    r = session.post("https://pennsylvaniastateparks.reserveamerica.com/" + next, data={"contractCode": "PA",
                                                                                        "parkId": "880414"})
    scrape(r.text, hold)

    return hold
