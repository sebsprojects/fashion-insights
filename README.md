## Overview

This project explores image data from fashion marketplaces with **Python** and Apache **Hadoop** and **Spark**. The goal of this project is to
- Learn more about Apache Hadoop and Spark
- Explore data engineering techniques
- Produce insights and pretty plots for the data second-hand fashion marketplaces deal with

## Data

The data used for this project comprises images of fashion items (usually taken by mobile phones) as well as extracted metadata. Each data point consists of:
- A UUID and timestamp
- Between 1 and 5 images in JPEG format (image-0.jpg, image-1.jpg, image-2.jpg, ...). Most images are smaller than 1MB (upper boundary is 15MB). For each image:
  - A list of labels (strings) describing objects in the image together with a confidence score and at least one bounding box
  - A set of strings that represents text (fragments) extracted from the image together with a confidence score
- The assumption is that each set of images shows exactly one object of interest. Thus, there is a list of predicted product types (list of strings) that are mutually exclusive and ordered with decreasing confidence  
- Similarly, for each set of images there are lists of predicted sizes, brands and colors that each have mutually exclusive entries and are ordered with decreasing confidence

Omitting the actual image data, a data point that consists of three images of a "BDG Urban Outfitters" Jeans size W31/L32 looks like this:
```
  uuid = 0c30e823d3037ea7
  timestamp = 2024-03-27T13:41:53.182Z
  
  image-0.jpg
      labels = [("Clothing", 100), ("Jeans", 99.98, <BoundingBox>), ("Handbag", 94.59), ...]
      text = [("AY", 100), ("NAY", 54.01), ("HAY", 53.63)]
  image-1.jpg
      labels = [("Pants", 100), ("Shorts", 99.99), ("Jacket", 99.21, <BoundingBox>), ...]
      text = [("BDG", 100), ("URBAN", 98.66), ("OUTFITTERS", 98.25), ...]
  image-2.jpg
      labels = [("Clothing", 99.09), ("Number", 55.64), ("Text", 55.64), ...]
      text = [("BDG", 100), ("W31", 99.81), ("L32", 99.97), ...]
  
  productTypes = ["Jeans", "Dress_pants", "Leggings", "Sweatpants"]
  colors = ["blue", "black", "grey", "white", "beige"]
  brands = ["BDG", "HAY", "Away", "AYMT", "Maya"]
  sizes = ["W31", "L32"]
```

The dataset contains more than 100,000 datapoints with a total size of more than 300GB. Unfortunately, this data is proprietary and I can't publicly elaborate on its origins nor share it.