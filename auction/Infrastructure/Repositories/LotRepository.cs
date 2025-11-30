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
            .FirstOrDefaultAsync(l=>l.Id == lotId);
    }

    public Task AddAsync(Lot lot)
    {
         _context.Lots.Add(lot);
        _context.SaveChangesAsync();
        return Task.CompletedTask;
    }

    public Task UpdateAsync(Lot lot)
    {
        _context.Lots.Update(lot);
        _context.SaveChangesAsync();
        return Task.CompletedTask;
    }

    public Task DeleteAsync(Lot lot)
    {
        lot.IsDeleted = true;
        _context.Lots.Update(lot);
        _context.SaveChangesAsync();
        return Task.CompletedTask;
    }
    
    
}