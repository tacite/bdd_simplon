from clean_csv import clean_csv


def main():
    df = clean_csv()
    print(df.head)


    
if __name__ == "__main__":
    main()