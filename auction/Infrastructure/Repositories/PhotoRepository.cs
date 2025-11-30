using Domain.Entities;
using Infrastructure.Data;
using Infrastructure.Interfaces;
using Microsoft.EntityFrameworkCore;

namespace Infrastructure.Repositories;

public class PhotoRepository : IPhotoRepository
{
    private readonly DataContext _context;

    public PhotoRepository(DataContext context)
    {
        _context = context;
    }

    public async Task<List<Photo>> GetByLotIdAsync(Guid lotId)
    {
        return await _context.Photos
            .Where(p => p.LotId == lotId)
            .OrderBy(p => p.Order)
            .ToListAsync();
    }

    public async Task AddAsync(Photo photo)
    {
        await _context.Photos.AddAsync(photo);
    }

    public async Task DeleteAsync(Guid lotId, string url)
    {
        var entity = await _context.Photos
            .FirstOrDefaultAsync(p => p.LotId == lotId && p.Url == url);

        if (entity != null)
            _context.Photos.Remove(entity);
    }

    public Task SaveChangesAsync()
    {
        return _context.SaveChangesAsync();
    }
}