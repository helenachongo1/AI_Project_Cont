import pandas as pd

# Load the BookShop dataset
df = pd.read_csv("C:/Users/Acer/Downloads/BookShop.csv")

'''# 1. Most popular/famous author
print("Based on ratings:")
print(df.groupby('Author')['Rating'].mean().idxmax())

print("\n Based on sales:")
print(df.groupby('Author')['Sales'].sum().idxmax())

# 2. Top-3 countries with highest number of authors
print("\n2. Top-3 countries with most authors:")
print(df['Country'].value_counts().head(3))

# 3. Hardworking author (most working hours per day)
print("\n3. Hardworking author:")
print(df.groupby('Author')['WorkingHoursPerDay'].mean().idxmax())

# 4. Top-5 authors with highest average ratings
print("\n4. Top-5 authors by average rating:")
print(df.groupby('Author')['Rating'].mean().sort_values(ascending=False).head(5))

# 5. Top-5 books with highest average ratings
print("\n5. Top-5 books by average rating:")
print(df.groupby('Book')['Rating'].mean().sort_values(ascending=False).head(5))

# 6. Top-5 authors spending max on marketing
print("\n6. Top-5 authors by marketing spend:")
print(df.groupby('Author')['MarketingCost'].sum().sort_values(ascending=False).head(5))

# 7. Top-5 authors by total pages written
print("\n7. Top-5 authors by total pages:")
print(df.groupby('Author')['Pages'].sum().sort_values(ascending=False).head(5))'''

# 8. Top-5 publication houses by book count
print("\n8. Top-5 publication houses by book count:")
print(df['PublicationHouse'].value_counts().head(5))

# 9. Top-5 publication houses by highest priced books
print("\n9. Top-5 publication houses by max price:")
print(df.groupby('PublicationHouse')['Price'].max().sort_values(ascending=False).head(5))

# 10. Total books in each genre
print("\n10. Book count per genre:")
print(df['Genre'].value_counts())

# 11. Top-5 publication houses with highest sales in each quarter
print("\n11. Top-5 publication houses by sales per quarter:")
for q in df['Quarter'].unique():
    print(f"\nQuarter {q}:")
    print(df[df['Quarter'] == q].groupby('PublicationHouse')['Sales'].sum().sort_values(ascending=False).head(5))

# 12. Top-3 youngest authors
print("\n12. Top-3 youngest authors:")
print(df[['Author', 'Age']].drop_duplicates().sort_values(by='Age').head(3))

# 13. Author whose book is least read
print("\n13. Least read author's book:")
print(df.groupby('Author')['Readers'].sum().idxmin())

# 14. Avg price of books by top-5 most-published authors
top5_authors = df['Author'].value_counts().head(5).index
print("\n14. Avg price by top-5 published authors:")
print(df[df['Author'].isin(top5_authors)].groupby('Author')['Price'].mean())

# 15. Avg price per publication house
print("\n15. Avg price per publication house:")
print(df.groupby('PublicationHouse')['Price'].mean())

# 16. Genre with highest sales
print("\n16. Genre with highest total sales:")
print(df.groupby('Genre')['Sales'].sum().idxmax())

# 17. Top-5 books with most awards
print("\n17. Top-5 awarded books:")
print(df.groupby('Book')['Awards'].sum().sort_values(ascending=False).head(5))

# 18. Top-3 publication houses with most awards
print("\n18. Top-3 publication houses by total awards:")
print(df.groupby('PublicationHouse')['Awards'].sum().sort_values(ascending=False).head(3))

# 19. Genre with highest average price
print("\n19. Genre with highest average price:")
print(df.groupby('Genre')['Price'].mean().idxmax())

# 20. Books published by houses with price > 20 USD
print("\n20. Books count by publication house with price > 20:")
print(df[df['Price'] > 20].groupby('PublicationHouse').size())

# 21. Top-5 books with highest worth (price/pages)
df['Worth'] = df['Price'] / df['Pages']
print("\n21. Top-5 books by worth:")
print(df[['Book', 'Worth']].drop_duplicates().sort_values(by='Worth', ascending=False).head(5))

# 22. Top-5 authors by total sales
print("\n22. Top-5 authors by sales:")
print(df.groupby('Author')['Sales'].sum().sort_values(ascending=False).head(5))

# 23. Top-5 books by number of pages
print("\n23. Top-5 books with most pages:")
print(df[['Book', 'Pages']].drop_duplicates().sort_values(by='Pages', ascending=False).head(5))