{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMnO4Tb5ndpo9bvPzr7dXeq",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/omvaghela/Dictionary/blob/main/All_done_The_Hindu_Program.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "from reportlab.lib.pagesizes import letter, landscape\n",
        "from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak\n",
        "from reportlab.lib import colors\n",
        "from reportlab.lib.styles import getSampleStyleSheet\n",
        "\n",
        "# Define the URL to scrape\n",
        "url = \"https://www.thehindu.com/opinion/editorial/\"\n",
        "\n",
        "# Create a session object\n",
        "session = requests.Session()\n",
        "\n",
        "# Send a GET request to the URL using the session object\n",
        "response = session.get(url)\n",
        "\n",
        "# Parse the HTML content\n",
        "soup = BeautifulSoup(response.content, \"html.parser\")\n",
        "\n",
        "# Extract the opinion articles section from the HTML\n",
        "opinion_section = soup.find(\"div\", {\"class\": \"col-xl-8 col-lg-8 col-md-8 col-sm-12 col-12\"})\n",
        "\n",
        "# Check if opinion section is found\n",
        "if opinion_section:\n",
        "    # Extract the opinion articles from the opinion section\n",
        "    opinion_articles = opinion_section.find_all(\"a\")\n",
        "\n",
        "    # Create a set to store processed article URLs\n",
        "    processed_urls = set()\n",
        "\n",
        "    # Create a PDF document\n",
        "    doc = SimpleDocTemplate(\"opinion_articles.pdf\", pagesize=landscape(letter))\n",
        "    doc.pagesize = landscape(letter)\n",
        "    elements = []\n",
        "\n",
        "    # Define styles for the document\n",
        "    styles = getSampleStyleSheet()\n",
        "    title_style = styles[\"Title\"]\n",
        "    text_style = styles[\"Normal\"]\n",
        "\n",
        "    # Loop through the opinion articles\n",
        "    for article in opinion_articles:\n",
        "        # Extract the URL of the linked webpage\n",
        "        article_url = article[\"href\"]\n",
        "\n",
        "        # Check if article URL has already been processed\n",
        "        if article_url in processed_urls:\n",
        "            continue  # Skip if already processed\n",
        "\n",
        "        # Clear all cookies from the session object\n",
        "        session.cookies.clear()\n",
        "\n",
        "        # Send a GET request to the article URL using the session object\n",
        "        article_response = session.get(article_url)\n",
        "\n",
        "        # Parse the HTML content of the article webpage\n",
        "        article_soup = BeautifulSoup(article_response.content, \"html.parser\")\n",
        "\n",
        "        # Extract the title of the article\n",
        "        article_title = article_soup.find(\"h1\", {\"itemprop\": \"name\", \"class\": \"title\"}).get_text().strip()\n",
        "\n",
        "        # Extract the article text from the article webpage\n",
        "        article_text_div = article_soup.find(\"div\", {\"class\": \"articlebodycontent col-xl-9 col-lg-12 col-md-12 col-sm-12 col-12\"})\n",
        "\n",
        "        # Check if article text div is found\n",
        "        if article_text_div:\n",
        "            # Extract the text from the <p> tags within the article text div\n",
        "            article_text = \"\\n\".join([p.get_text().strip() for p in article_text_div.find_all(\"p\")])\n",
        "\n",
        "            # Remove text after \"SHARE\" word\n",
        "            share_index = article_text.find(\"SHARE\")\n",
        "            if share_index != -1:\n",
        "                article_text = article_text[:share_index]\n",
        "\n",
        "            # Add article title to the document\n",
        "            elements.append(Paragraph(article_title, title_style))\n",
        "\n",
        "            # Add article text to the document\n",
        "            elements.append(Paragraph(article_text, text_style))\n",
        "\n",
        "            # Add a page break after each article\n",
        "            elements.append(PageBreak())\n",
        "\n",
        "            # Add article URL to processed URLs\n",
        "            processed_urls.add(article_url)\n",
        "        else:\n",
        "            print(\"No article text found for URL:\", article_url)\n",
        "\n",
        "    # Build the document\n",
        "    doc.build(elements)\n",
        "\n",
        "    print(\"PDF created successfully!\")\n",
        "else:\n",
        "    print(\"No opinion articles found on the webpage.\")\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "MvkFO8Za5cqU",
        "outputId": "5d6cdd0c-29da-43ed-9910-35f04507f90f"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "PDF created successfully!\n"
          ]
        }
      ]
    }
  ]
}