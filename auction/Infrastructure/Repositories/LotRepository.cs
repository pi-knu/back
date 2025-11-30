using Domain.Entities;
using Infrastructure.Data;
using Infrastructure.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories;

public class LotRepository : ILotRepository
{
    private readonly DataContext _context;

    public LotRepository(DataContext context)
    {
        _context = context;
    }

    public async Task<Lot?> GetByIdAsync(Guid lotId)
    {
        return await _context.Lots
            .FirstOrDefaultAsync(l => l.Id == lotId);
    }

    public async Task AddAsync(Lot lot)
    {
        await _context.Lots.AddAsync(lot);
    }

    public Task UpdateAsync(Lot lot)
    {
        _context.Lots.Update(lot);
        return Task.CompletedTask;
    }

    public Task SoftDeleteAsync(Lot lot)
    {
        lot.IsDeleted = true;
        lot.IsActive = false;
        _context.Lots.Update(lot);
        return Task.CompletedTask;
    }

    public Task SaveChangesAsync()
    {
        return _context.SaveChangesAsync();
    }
}