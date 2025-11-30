using Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Data;

public class DataContext : DbContext
{
    public DataContext(DbContextOptions<DataContext> options) : base(options)
    {
    }

    public DbSet<Lot> Lots { get; set; }
    public DbSet<Bid> Bids { get; set; }
    public DbSet<Photo> Photos { get; set; }
    public DbSet<Auction> Auctions { get; set; }

}