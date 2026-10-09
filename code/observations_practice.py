import csv

def load_observations(path):
    with open(path, newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))

def parse_count(count_text):
   if not isinstance(count_text, str):
           raise ValueError("Count must be text")
   if count_text == "":
       return None #return None for missing count
   count = int(count_text) #return an integer for a valid count
   if count < 0:
      raise ValueError("Count cannot be negative") #return ValueError for an invalid count    
   return count #return the count if it's valid


def summarise_site(rows, site):
   return(None, 0)


if __name__ == "__main__":
    rows = load_observations("data/bootcamp_observations.csv")
    print(rows[0])
    print(rows[2])


