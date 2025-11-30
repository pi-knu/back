using Domain.Entities;

namespace Infrastructure.Interfaces;

public interface IPhotoRepository
{
    Task<List<Photo>> GetByLotIdAsync(Guid lotId);
    Task AddAsync(Photo photo);
    Task DeleteAsync(Guid lotId, string url);
    Task SaveChangesAsync();
}
