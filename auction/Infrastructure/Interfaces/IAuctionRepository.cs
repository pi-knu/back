using Domain.Entities;

namespace Infrastructure.Interfaces;

public interface IAuctionRepository
{
    Task<Auction?> GetByIdAsync(Guid auctionId);
    Task AddAsync(Auction auction);
    Task UpdateAsync(Auction auction);
    Task SaveChangesAsync();
}