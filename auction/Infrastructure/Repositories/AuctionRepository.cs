using Domain.Entities;
using Infrastructure.Data;
using Infrastructure.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories;

public class AuctionRepository : IAuctionRepository
{
    private readonly DataContext _context;

    public AuctionRepository(DataContext context)
    {
        _context = context;
    }

    public async Task<Auction?> GetByIdAsync(Guid auctionId)
    {
        return await _context.Auctions
            .FirstOrDefaultAsync(a => a.Id == auctionId);
    }

    public async Task AddAsync(Auction auction)
    {
        await _context.Auctions.AddAsync(auction);
    }

    public Task UpdateAsync(Auction auction)
    {
        _context.Auctions.Update(auction);
        return Task.CompletedTask;
    }

    public Task SaveChangesAsync()
    {
        return _context.SaveChangesAsync();
    }
}