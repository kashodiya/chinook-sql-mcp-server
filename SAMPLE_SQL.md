# Complex Sample Questions and SQL Queries

## 1. Which artists have the highest total sales revenue?
```sql
SELECT ar.Name, SUM(il.UnitPrice * il.Quantity) as TotalRevenue
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY ar.ArtistId, ar.Name
ORDER BY TotalRevenue DESC
LIMIT 10;
```

## 2. What are the top 5 countries by total number of customers and their average invoice value?
```sql
SELECT c.Country, 
       COUNT(DISTINCT c.CustomerId) as CustomerCount,
       AVG(i.Total) as AvgInvoiceValue,
       SUM(i.Total) as TotalRevenue
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.Country
ORDER BY CustomerCount DESC, TotalRevenue DESC
LIMIT 5;
```

## 3. Which employees have generated the most sales and how many customers do they support?
```sql
SELECT e.FirstName || ' ' || e.LastName as EmployeeName,
       COUNT(DISTINCT c.CustomerId) as CustomersSupported,
       COUNT(i.InvoiceId) as TotalInvoices,
       SUM(i.Total) as TotalSales
FROM Employee e
JOIN Customer c ON e.EmployeeId = c.SupportRepId
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY e.EmployeeId
ORDER BY TotalSales DESC;
```

## 4. What is the most popular genre by number of tracks sold in each country?
```sql
WITH GenreCountryStats AS (
    SELECT c.Country, g.Name as Genre,
           COUNT(il.InvoiceLineId) as TracksSold,
           ROW_NUMBER() OVER (PARTITION BY c.Country ORDER BY COUNT(il.InvoiceLineId) DESC) as rn
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
    JOIN Track t ON il.TrackId = t.TrackId
    JOIN Genre g ON t.GenreId = g.GenreId
    GROUP BY c.Country, g.GenreId, g.Name
)
SELECT Country, Genre, TracksSold
FROM GenreCountryStats
WHERE rn = 1
ORDER BY TracksSold DESC;
```

## 5. Which albums have tracks in multiple playlists and what's their cross-playlist popularity?
```sql
SELECT al.Title as AlbumTitle, ar.Name as ArtistName,
       COUNT(DISTINCT pt.PlaylistId) as PlaylistCount,
       COUNT(pt.TrackId) as TotalPlaylistAppearances,
       COUNT(DISTINCT t.TrackId) as TracksInPlaylists
FROM Album al
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
GROUP BY al.AlbumId
HAVING COUNT(DISTINCT pt.PlaylistId) > 1
ORDER BY PlaylistCount DESC, TotalPlaylistAppearances DESC;
```

## 6. What's the monthly sales trend for the last 2 years with year-over-year comparison?
```sql
SELECT strftime('%Y', InvoiceDate) as Year,
       strftime('%m', InvoiceDate) as Month,
       COUNT(InvoiceId) as InvoiceCount,
       SUM(Total) as MonthlyRevenue,
       LAG(SUM(Total), 12) OVER (ORDER BY strftime('%Y-%m', InvoiceDate)) as PreviousYearRevenue
FROM Invoice
WHERE InvoiceDate >= date('now', '-2 years')
GROUP BY strftime('%Y-%m', InvoiceDate)
ORDER BY Year, Month;
```

## 7. Which customers have purchased tracks from the most diverse set of genres?
```sql
SELECT c.FirstName || ' ' || c.LastName as CustomerName,
       c.Email,
       COUNT(DISTINCT g.GenreId) as GenresDiversity,
       COUNT(il.InvoiceLineId) as TotalTracksPurchased,
       SUM(il.UnitPrice * il.Quantity) as TotalSpent
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY c.CustomerId
ORDER BY GenresDiversity DESC, TotalSpent DESC
LIMIT 15;
```

## 8. What's the average track length and price by media type and genre combination?
```sql
SELECT mt.Name as MediaType, g.Name as Genre,
       COUNT(t.TrackId) as TrackCount,
       AVG(t.Milliseconds/1000.0/60.0) as AvgLengthMinutes,
       AVG(t.UnitPrice) as AvgPrice,
       SUM(COALESCE(il.Quantity, 0)) as TotalSold
FROM MediaType mt
CROSS JOIN Genre g
LEFT JOIN Track t ON mt.MediaTypeId = t.MediaTypeId AND g.GenreId = t.GenreId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
WHERE t.TrackId IS NOT NULL
GROUP BY mt.MediaTypeId, g.GenreId
HAVING TrackCount > 5
ORDER BY MediaType, Genre;
```

## 9. Which artists have the most tracks in customer playlists vs. actual purchases?
```sql
SELECT ar.Name as ArtistName,
       COUNT(DISTINCT pt.TrackId) as TracksInPlaylists,
       COUNT(DISTINCT il.TrackId) as TracksPurchased,
       CASE 
           WHEN COUNT(DISTINCT il.TrackId) > 0 
           THEN ROUND(COUNT(DISTINCT pt.TrackId) * 1.0 / COUNT(DISTINCT il.TrackId), 2)
           ELSE 0 
       END as PlaylistToPurchaseRatio
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
LEFT JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY ar.ArtistId
HAVING TracksInPlaylists > 0 OR TracksPurchased > 0
ORDER BY PlaylistToPurchaseRatio DESC, TracksInPlaylists DESC;
```

## 10. What's the customer lifetime value distribution and retention analysis?
```sql
WITH CustomerStats AS (
    SELECT c.CustomerId,
           c.FirstName || ' ' || c.LastName as CustomerName,
           MIN(i.InvoiceDate) as FirstPurchase,
           MAX(i.InvoiceDate) as LastPurchase,
           COUNT(i.InvoiceId) as TotalInvoices,
           SUM(i.Total) as LifetimeValue,
           julianday(MAX(i.InvoiceDate)) - julianday(MIN(i.InvoiceDate)) as CustomerLifespanDays
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
)
SELECT 
    CASE 
        WHEN LifetimeValue < 10 THEN 'Low Value (<$10)'
        WHEN LifetimeValue < 25 THEN 'Medium Value ($10-$25)'
        WHEN LifetimeValue < 50 THEN 'High Value ($25-$50)'
        ELSE 'Premium Value (>$50)'
    END as ValueSegment,
    COUNT(*) as CustomerCount,
    AVG(LifetimeValue) as AvgLifetimeValue,
    AVG(CustomerLifespanDays) as AvgLifespanDays,
    AVG(TotalInvoices) as AvgInvoices
FROM CustomerStats
GROUP BY ValueSegment
ORDER BY AvgLifetimeValue DESC;
```

## 11. Which tracks have the highest price-to-length ratio and are they popular?
```sql
SELECT t.Name as TrackName, ar.Name as ArtistName, al.Title as AlbumTitle,
       t.UnitPrice, 
       t.Milliseconds/1000.0/60.0 as LengthMinutes,
       ROUND(t.UnitPrice / (t.Milliseconds/1000.0/60.0), 4) as PricePerMinute,
       COUNT(il.InvoiceLineId) as TimesPurchased,
       COUNT(pt.PlaylistId) as PlaylistAppearances
FROM Track t
JOIN Album al ON t.AlbumId = al.AlbumId
JOIN Artist ar ON al.ArtistId = ar.ArtistId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
LEFT JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
WHERE t.Milliseconds > 0
GROUP BY t.TrackId
ORDER BY PricePerMinute DESC
LIMIT 20;
```

## 12. What's the seasonal purchasing pattern by genre?
```sql
SELECT g.Name as Genre,
       CASE 
           WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) IN (12, 1, 2) THEN 'Winter'
           WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) IN (3, 4, 5) THEN 'Spring'
           WHEN CAST(strftime('%m', i.InvoiceDate) AS INTEGER) IN (6, 7, 8) THEN 'Summer'
           ELSE 'Fall'
       END as Season,
       COUNT(il.InvoiceLineId) as TracksSold,
       SUM(il.UnitPrice * il.Quantity) as Revenue
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
JOIN Invoice i ON il.InvoiceId = i.InvoiceId
GROUP BY g.GenreId, Season
ORDER BY g.Name, 
         CASE Season 
             WHEN 'Spring' THEN 1 
             WHEN 'Summer' THEN 2 
             WHEN 'Fall' THEN 3 
             WHEN 'Winter' THEN 4 
         END;
```

## 13. Which employees manage customers with the highest average order values?
```sql
SELECT e.FirstName || ' ' || e.LastName as EmployeeName,
       e.Title,
       COUNT(DISTINCT c.CustomerId) as CustomersManaged,
       COUNT(i.InvoiceId) as TotalInvoices,
       AVG(i.Total) as AvgOrderValue,
       SUM(i.Total) as TotalRevenue,
       MAX(i.Total) as LargestOrder
FROM Employee e
JOIN Customer c ON e.EmployeeId = c.SupportRepId
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY e.EmployeeId
ORDER BY AvgOrderValue DESC;
```

## 14. What's the correlation between album track count and commercial success?
```sql
SELECT al.Title as AlbumTitle, ar.Name as ArtistName,
       COUNT(t.TrackId) as TrackCount,
       COUNT(il.InvoiceLineId) as TotalTracksSold,
       SUM(il.UnitPrice * il.Quantity) as AlbumRevenue,
       ROUND(COUNT(il.InvoiceLineId) * 1.0 / COUNT(t.TrackId), 2) as SalesPerTrack,
       COUNT(DISTINCT pt.PlaylistId) as PlaylistsContainingTracks
FROM Album al
JOIN Artist ar ON al.ArtistId = ar.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
LEFT JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
GROUP BY al.AlbumId
HAVING TrackCount > 1
ORDER BY SalesPerTrack DESC, AlbumRevenue DESC;
```

## 15. Which cities have the most diverse music taste based on genre purchases?
```sql
SELECT c.City, c.Country,
       COUNT(DISTINCT c.CustomerId) as CustomerCount,
       COUNT(DISTINCT g.GenreId) as GenresDiversity,
       COUNT(il.InvoiceLineId) as TotalTracksPurchased,
       SUM(il.UnitPrice * il.Quantity) as TotalRevenue,
       ROUND(COUNT(DISTINCT g.GenreId) * 1.0 / COUNT(DISTINCT c.CustomerId), 2) as GenresPerCustomer
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
JOIN InvoiceLine il ON i.InvoiceId = il.InvoiceId
JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
WHERE c.City IS NOT NULL
GROUP BY c.City, c.Country
HAVING CustomerCount >= 2
ORDER BY GenresDiversity DESC, GenresPerCustomer DESC;
```

## 16. What's the track completion rate in playlists vs. purchase behavior?
```sql
WITH PlaylistStats AS (
    SELECT p.Name as PlaylistName,
           COUNT(pt.TrackId) as TracksInPlaylist,
           COUNT(DISTINCT t.AlbumId) as AlbumsRepresented,
           COUNT(DISTINCT ar.ArtistId) as ArtistsRepresented
    FROM Playlist p
    JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
    JOIN Track t ON pt.TrackId = t.TrackId
    JOIN Album al ON t.AlbumId = al.AlbumId
    JOIN Artist ar ON al.ArtistId = ar.ArtistId
    GROUP BY p.PlaylistId
),
PurchaseStats AS (
    SELECT p.Name as PlaylistName,
           COUNT(il.InvoiceLineId) as TracksPurchased,
           SUM(il.UnitPrice * il.Quantity) as PlaylistRevenue
    FROM Playlist p
    JOIN PlaylistTrack pt ON p.PlaylistId = pt.PlaylistId
    JOIN InvoiceLine il ON pt.TrackId = il.TrackId
    GROUP BY p.PlaylistId
)
SELECT ps.PlaylistName,
       ps.TracksInPlaylist,
       ps.AlbumsRepresented,
       ps.ArtistsRepresented,
       COALESCE(pus.TracksPurchased, 0) as TracksPurchased,
       COALESCE(pus.PlaylistRevenue, 0) as PlaylistRevenue,
       CASE 
           WHEN ps.TracksInPlaylist > 0 
           THEN ROUND(COALESCE(pus.TracksPurchased, 0) * 100.0 / ps.TracksInPlaylist, 2)
           ELSE 0 
       END as PurchaseRate
FROM PlaylistStats ps
LEFT JOIN PurchaseStats pus ON ps.PlaylistName = pus.PlaylistName
ORDER BY PurchaseRate DESC, PlaylistRevenue DESC;
```

## 17. Which composers have the most commercially successful tracks across different genres?
```sql
SELECT t.Composer,
       COUNT(DISTINCT g.GenreId) as GenresDiversity,
       COUNT(DISTINCT t.TrackId) as TotalTracks,
       COUNT(il.InvoiceLineId) as TracksSold,
       SUM(il.UnitPrice * il.Quantity) as TotalRevenue,
       AVG(t.Milliseconds/1000.0/60.0) as AvgTrackLengthMinutes,
       COUNT(DISTINCT pt.PlaylistId) as PlaylistsAppearances
FROM Track t
LEFT JOIN Genre g ON t.GenreId = g.GenreId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
LEFT JOIN PlaylistTrack pt ON t.TrackId = pt.TrackId
WHERE t.Composer IS NOT NULL AND t.Composer != ''
GROUP BY t.Composer
HAVING TotalTracks >= 5
ORDER BY TotalRevenue DESC, GenresDiversity DESC;
```

## 18. What's the customer churn analysis based on purchase intervals?
```sql
WITH CustomerPurchaseIntervals AS (
    SELECT c.CustomerId,
           c.FirstName || ' ' || c.LastName as CustomerName,
           i.InvoiceDate,
           LAG(i.InvoiceDate) OVER (PARTITION BY c.CustomerId ORDER BY i.InvoiceDate) as PreviousInvoiceDate,
           julianday(i.InvoiceDate) - julianday(LAG(i.InvoiceDate) OVER (PARTITION BY c.CustomerId ORDER BY i.InvoiceDate)) as DaysBetweenPurchases
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
),
CustomerChurnAnalysis AS (
    SELECT CustomerId,
           CustomerName,
           COUNT(*) as TotalIntervals,
           AVG(DaysBetweenPurchases) as AvgDaysBetweenPurchases,
           MAX(DaysBetweenPurchases) as MaxDaysBetweenPurchases,
           MIN(DaysBetweenPurchases) as MinDaysBetweenPurchases,
           MAX(InvoiceDate) as LastPurchaseDate,
           julianday('now') - julianday(MAX(InvoiceDate)) as DaysSinceLastPurchase
    FROM CustomerPurchaseIntervals
    WHERE DaysBetweenPurchases IS NOT NULL
    GROUP BY CustomerId, CustomerName
)
SELECT 
    CASE 
        WHEN DaysSinceLastPurchase <= 30 THEN 'Active (0-30 days)'
        WHEN DaysSinceLastPurchase <= 90 THEN 'At Risk (31-90 days)'
        WHEN DaysSinceLastPurchase <= 180 THEN 'Dormant (91-180 days)'
        ELSE 'Churned (>180 days)'
    END as CustomerStatus,
    COUNT(*) as CustomerCount,
    AVG(AvgDaysBetweenPurchases) as AvgPurchaseInterval,
    AVG(DaysSinceLastPurchase) as AvgDaysSinceLastPurchase
FROM CustomerChurnAnalysis
GROUP BY CustomerStatus
ORDER BY 
    CASE CustomerStatus
        WHEN 'Active (0-30 days)' THEN 1
        WHEN 'At Risk (31-90 days)' THEN 2
        WHEN 'Dormant (91-180 days)' THEN 3
        WHEN 'Churned (>180 days)' THEN 4
    END;
```

## 19. Which media types and genres combination have the best profit margins?
```sql
SELECT mt.Name as MediaType, g.Name as Genre,
       COUNT(DISTINCT t.TrackId) as TrackCount,
       AVG(t.UnitPrice) as AvgTrackPrice,
       SUM(il.Quantity) as TotalUnitsSold,
       SUM(il.UnitPrice * il.Quantity) as TotalRevenue,
       AVG(t.Bytes/1024.0/1024.0) as AvgFileSizeMB,
       ROUND(SUM(il.UnitPrice * il.Quantity) / COUNT(DISTINCT t.TrackId), 2) as RevenuePerTrack
FROM MediaType mt
JOIN Track t ON mt.MediaTypeId = t.MediaTypeId
JOIN Genre g ON t.GenreId = g.GenreId
LEFT JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY mt.MediaTypeId, g.GenreId
HAVING TrackCount >= 10 AND TotalUnitsSold > 0
ORDER BY RevenuePerTrack DESC, TotalRevenue DESC;
```

## 20. What's the hierarchical analysis of employee performance and their customer relationships?
```sql
WITH EmployeeHierarchy AS (
    SELECT e1.EmployeeId, 
           e1.FirstName || ' ' || e1.LastName as EmployeeName,
           e1.Title,
           e2.FirstName || ' ' || e2.LastName as ManagerName,
           e2.Title as ManagerTitle
    FROM Employee e1
    LEFT JOIN Employee e2 ON e1.ReportsTo = e2.EmployeeId
),
EmployeePerformance AS (
    SELECT e.EmployeeId,
           COUNT(DISTINCT c.CustomerId) as DirectCustomers,
           COUNT(i.InvoiceId) as TotalInvoices,
           SUM(i.Total) as TotalRevenue,
           AVG(i.Total) as AvgInvoiceValue,
           MAX(i.InvoiceDate) as LastSaleDate
    FROM Employee e
    LEFT JOIN Customer c ON e.EmployeeId = c.SupportRepId
    LEFT JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY e.EmployeeId
)
SELECT eh.EmployeeName,
       eh.Title,
       eh.ManagerName,
       eh.ManagerTitle,
       COALESCE(ep.DirectCustomers, 0) as DirectCustomers,
       COALESCE(ep.TotalInvoices, 0) as TotalInvoices,
       COALESCE(ep.TotalRevenue, 0) as TotalRevenue,
       COALESCE(ep.AvgInvoiceValue, 0) as AvgInvoiceValue,
       ep.LastSaleDate,
       CASE 
           WHEN ep.LastSaleDate IS NULL THEN 'No Sales'
           WHEN julianday('now') - julianday(ep.LastSaleDate) <= 30 THEN 'Recent Activity'
           WHEN julianday('now') - julianday(ep.LastSaleDate) <= 90 THEN 'Moderate Activity'
           ELSE 'Low Activity'
       END as ActivityLevel
FROM EmployeeHierarchy eh
LEFT JOIN EmployeePerformance ep ON eh.EmployeeId = ep.EmployeeId
ORDER BY ep.TotalRevenue DESC NULLS LAST;
```