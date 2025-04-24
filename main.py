from core.scrape import get_data
import requests


def main():
    data = get_data()

    available_sites = [item for item in data if item['availability']]

    if len(available_sites) > 0:
        markdown_list = "\n".join(
            " - Site Number " + item['site_number'] for item in available_sites)
        markdown = f"""
        # List of Open Camp Spots
        {markdown_list}
        """

        topic = 'https://ntfy.moonspot.app/campground'
        requests.post(topic, data=markdown, headers={"Markdown": "yes"})
    else:
        print("No Campsites Available")


if __name__ == "__main__":
    main()
