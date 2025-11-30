using Domain.Entities;
using Infrastructure.Data;
using Infrastructure.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories;

public class BidRepository : IBidRepository
{
    private readonly DataContext _context;

    public BidRepository(DataContext context)
    {
        _context = context;
    }

    public async Task<List<Bid>> GetLast10BidsAsync(Guid auctionId)
    {
        return await _context.Bids
            .Where(b => b.AuctionId == auctionId && !b.IsAborted)
            .OrderByDescending(b => b.CreatedAt)
            .Take(10)
            .ToListAsync();
    }

    public async Task AddAsync(Bid bid)
    {
        await _context.Bids.AddAsync(bid);
    }

    public Task SaveChangesAsync()
    {
        return _context.SaveChangesAsync();
    }
}