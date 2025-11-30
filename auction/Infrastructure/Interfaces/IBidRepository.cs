using Domain.Entities;

namespace Infrastructure.Interfaces;

public interface IBidRepository
{
    Task<List<Bid>> GetLast10BidsAsync(Guid auctionId);
    Task AddAsync(Bid bid);
    Task SaveChangesAsync();
}