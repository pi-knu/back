using Domain.Entities;

namespace Infrastructure.Interfaces;

public interface ILotRepository
{
    Task<Lot?> GetByIdAsync(Guid lotId);
    Task AddAsync(Lot lot);
    Task UpdateAsync(Lot lot);
    Task DeleteAsync(Lot lot);
}