# Database Schema

## Album

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| AlbumId | INTEGER | Yes | NULL | Yes |
| Title | NVARCHAR(160) | Yes | NULL | No |
| ArtistId | INTEGER | Yes | NULL | No |

**Foreign Keys:**
- ArtistId -> Artist.ArtistId

## Artist

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| ArtistId | INTEGER | Yes | NULL | Yes |
| Name | NVARCHAR(120) | No | NULL | No |

## Customer

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| CustomerId | INTEGER | Yes | NULL | Yes |
| FirstName | NVARCHAR(40) | Yes | NULL | No |
| LastName | NVARCHAR(20) | Yes | NULL | No |
| Company | NVARCHAR(80) | No | NULL | No |
| Address | NVARCHAR(70) | No | NULL | No |
| City | NVARCHAR(40) | No | NULL | No |
| State | NVARCHAR(40) | No | NULL | No |
| Country | NVARCHAR(40) | No | NULL | No |
| PostalCode | NVARCHAR(10) | No | NULL | No |
| Phone | NVARCHAR(24) | No | NULL | No |
| Fax | NVARCHAR(24) | No | NULL | No |
| Email | NVARCHAR(60) | Yes | NULL | No |
| SupportRepId | INTEGER | No | NULL | No |

**Foreign Keys:**
- SupportRepId -> Employee.EmployeeId

## Employee

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| EmployeeId | INTEGER | Yes | NULL | Yes |
| LastName | NVARCHAR(20) | Yes | NULL | No |
| FirstName | NVARCHAR(20) | Yes | NULL | No |
| Title | NVARCHAR(30) | No | NULL | No |
| ReportsTo | INTEGER | No | NULL | No |
| BirthDate | DATETIME | No | NULL | No |
| HireDate | DATETIME | No | NULL | No |
| Address | NVARCHAR(70) | No | NULL | No |
| City | NVARCHAR(40) | No | NULL | No |
| State | NVARCHAR(40) | No | NULL | No |
| Country | NVARCHAR(40) | No | NULL | No |
| PostalCode | NVARCHAR(10) | No | NULL | No |
| Phone | NVARCHAR(24) | No | NULL | No |
| Fax | NVARCHAR(24) | No | NULL | No |
| Email | NVARCHAR(60) | No | NULL | No |

**Foreign Keys:**
- ReportsTo -> Employee.EmployeeId

## Genre

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| GenreId | INTEGER | Yes | NULL | Yes |
| Name | NVARCHAR(120) | No | NULL | No |

## Invoice

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| InvoiceId | INTEGER | Yes | NULL | Yes |
| CustomerId | INTEGER | Yes | NULL | No |
| InvoiceDate | DATETIME | Yes | NULL | No |
| BillingAddress | NVARCHAR(70) | No | NULL | No |
| BillingCity | NVARCHAR(40) | No | NULL | No |
| BillingState | NVARCHAR(40) | No | NULL | No |
| BillingCountry | NVARCHAR(40) | No | NULL | No |
| BillingPostalCode | NVARCHAR(10) | No | NULL | No |
| Total | NUMERIC(10,2) | Yes | NULL | No |

**Foreign Keys:**
- CustomerId -> Customer.CustomerId

## InvoiceLine

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| InvoiceLineId | INTEGER | Yes | NULL | Yes |
| InvoiceId | INTEGER | Yes | NULL | No |
| TrackId | INTEGER | Yes | NULL | No |
| UnitPrice | NUMERIC(10,2) | Yes | NULL | No |
| Quantity | INTEGER | Yes | NULL | No |

**Foreign Keys:**
- TrackId -> Track.TrackId
- InvoiceId -> Invoice.InvoiceId

## MediaType

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| MediaTypeId | INTEGER | Yes | NULL | Yes |
| Name | NVARCHAR(120) | No | NULL | No |

## Playlist

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| PlaylistId | INTEGER | Yes | NULL | Yes |
| Name | NVARCHAR(120) | No | NULL | No |

## PlaylistTrack

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| PlaylistId | INTEGER | Yes | NULL | Yes |
| TrackId | INTEGER | Yes | NULL | Yes |

**Foreign Keys:**
- TrackId -> Track.TrackId
- PlaylistId -> Playlist.PlaylistId

## Track

| Column | Type | Not Null | Default | Primary Key |
|--------|------|----------|---------|-------------|
| TrackId | INTEGER | Yes | NULL | Yes |
| Name | NVARCHAR(200) | Yes | NULL | No |
| AlbumId | INTEGER | No | NULL | No |
| MediaTypeId | INTEGER | Yes | NULL | No |
| GenreId | INTEGER | No | NULL | No |
| Composer | NVARCHAR(220) | No | NULL | No |
| Milliseconds | INTEGER | Yes | NULL | No |
| Bytes | INTEGER | No | NULL | No |
| UnitPrice | NUMERIC(10,2) | Yes | NULL | No |

**Foreign Keys:**
- MediaTypeId -> MediaType.MediaTypeId
- GenreId -> Genre.GenreId
- AlbumId -> Album.AlbumId

