from sgrequests import SgRequests
from bs4 import BeautifulSoup as bs
from sgscrape import simple_scraper_pipeline as sp


def get_data():
    url = "https://virgin.know-where.com/virginplus/cgi/selection?place=Ajax%2C%20ON%20L1T%2C%20Canada&lang=en&ll=43.8776305%2C-79.04755589999999&async=results&stype=ll"
    session = SgRequests()

    response = session.get(url).text
    soup = bs(response, "html.parser")

    grids = soup.find_all("td", attrs={"class": "kw-results-info"})

    for grid in grids:
        locator_domain = "virginmobile.ca"

        try:
            page_url = grid.find("li", attrs={"class": "kw-appointment-icon kw-results-icon-list-element"}).find("a")["href"]
        except Exception:
            page_url = "<MISSING>"
        
        location_name = grid.find("span", attrs={"class": "kw-results-FIELD-NAME ultra"}).text.strip().split(" - ")[0].strip()

        address = grid.find("span", attrs={"class": "kw-tablify-address"}).text.strip()

        latitude = "<LATER>"
        longitude = "<LATER>"

        city_state_zipp = soup.find("span", attrs={"class": "kw-tablify-city-state"}).text.strip()
        
        city = city_state_zipp.split(",")[0]
        store_number = grid["data-kwsite"]

        state = city_state_zipp.split(", ")[1].split(" ")[0]
        zipp = city_state_zipp.split(", ")[1].split(" ")[1]

        phone = "<LATER>"
        location_type = "<LATER>"
        hours = "<LATER>"
        country_code = "<LATER>"

        yield {
            "locator_domain": locator_domain,
            "page_url": page_url,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "city": city,
            "store_number": store_number,
            "street_address": address,
            "state": state,
            "zip": zipp,
            "phone": phone,
            "location_type": location_type,
            "hours": hours,
            "country_code": country_code,
        }

def scrape():
    field_defs = sp.SimpleScraperPipeline.field_definitions(
        locator_domain=sp.MappingField(mapping=["locator_domain"]),
        page_url=sp.MappingField(mapping=["page_url"], part_of_record_identity=True),
        location_name=sp.MappingField(
            mapping=["location_name"], part_of_record_identity=True
        ),
        latitude=sp.MappingField(mapping=["latitude"], part_of_record_identity=True),
        longitude=sp.MappingField(mapping=["longitude"], part_of_record_identity=True),
        street_address=sp.MultiMappingField(
            mapping=["street_address"], is_required=False
        ),
        city=sp.MappingField(
            mapping=["city"],
        ),
        state=sp.MappingField(mapping=["state"], is_required=False),
        zipcode=sp.MultiMappingField(mapping=["zip"], is_required=False),
        country_code=sp.MappingField(mapping=["country_code"]),
        phone=sp.MappingField(mapping=["phone"], is_required=False),
        store_number=sp.MappingField(
            mapping=["store_number"], part_of_record_identity=True
        ),
        hours_of_operation=sp.MappingField(mapping=["hours"], is_required=False),
        location_type=sp.MappingField(mapping=["location_type"], is_required=False),
    )

    pipeline = sp.SimpleScraperPipeline(
        scraper_name="Crawler",
        data_fetcher=get_data,
        field_definitions=field_defs,
        log_stats_interval=15,
    )
    pipeline.run()


scrape()