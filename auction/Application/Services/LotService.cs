using Application.Dtos;
using Application.interfaces;
using Domain.Entities;
using Infrastructure.Interfaces;

namespace Application.Services;

public class LotService : ILotService
{
    private readonly ILotRepository _lotRepository;

    public LotService(ILotRepository lotRepository)
    {
        _lotRepository = lotRepository;
    }

    public async Task<LotResponseDto> AddLot(LotRequestDto dto)
    {
        var lot = new Lot
        {
            Id = Guid.NewGuid(),
            UserId = dto.UserId,
            Name = dto.Name,
            Description = dto.Description,
            IsDeleted = false,
            IsActive = true
        };

        await _lotRepository.AddAsync(lot);
        await _lotRepository.SaveChangesAsync();

        return new LotResponseDto(
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            IsDeleted: lot.IsDeleted,
            IsActive: lot.IsActive
        );
    }

    public async Task<LotResponseDto?> GetLotById(Guid lotId)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);

        if (lot == null || lot.IsDeleted)
            return null;

        return new LotResponseDto(
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            IsDeleted: lot.IsDeleted,
            IsActive: lot.IsActive
        );
    }

    public async Task<LotResponseDto?> UpdateLot(Guid lotId, LotUpdateDto dto)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);

        if (lot == null || lot.IsDeleted)
            return null;

        if (dto.Name != null)
            lot.Name = dto.Name;

        if (dto.Description != null)
            lot.Description = dto.Description;

        if (dto.IsActive.HasValue)
            lot.IsActive = dto.IsActive.Value;

        await _lotRepository.UpdateAsync(lot);
        await _lotRepository.SaveChangesAsync();

        return new LotResponseDto(
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            IsDeleted: lot.IsDeleted,
            IsActive: lot.IsActive
        );
    }

    public async Task<bool> DeleteLot(Guid lotId)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);
        if (lot == null)
            return false;

        lot.IsDeleted = true;
        lot.IsActive = false;

        await _lotRepository.UpdateAsync(lot);
        await _lotRepository.SaveChangesAsync();

        return true;
    }
}
