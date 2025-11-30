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

    public async Task<LotResponseDto> AddLot(LotRequestDto lotRequestDto)
    {
        var lot = new Lot()
        {
            Id = Guid.NewGuid(),
            UserId = lotRequestDto.UserId,
            Name = lotRequestDto.Name,
            Description = lotRequestDto.Description,
            MinPrice = lotRequestDto.MinPrice,
            MinStep = lotRequestDto.MinStep,
            CurrentPrice = lotRequestDto.MinPrice,
            IsDeleted = false,
            IsFinished = false
        };
        
        await _lotRepository.AddAsync(lot);
        var lotResponseDto = new LotResponseDto
        (
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            MinPrice: lot.MinPrice,
            MinStep: lot.MinStep,
            CurrentPrice: lot.CurrentPrice,
            IsDeleted: lot.IsDeleted,
            IsFinished: lot.IsFinished
        );
        
        return lotResponseDto;
    }

    public async Task<LotResponseDto?> GetLotById(Guid lotId)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);
        
        if (lot == null || lot.IsDeleted)
            return null;

        var lotResponseDto = new LotResponseDto
        (
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            MinPrice: lot.MinPrice,
            MinStep: lot.MinStep,
            CurrentPrice: lot.CurrentPrice,
            IsDeleted: lot.IsDeleted,
            IsFinished: lot.IsFinished
        );
        
        return lotResponseDto;
    }

    public async Task<LotResponseDto?> UpdateLot(Guid lotId, LotUpdateDto lotUpdateDto)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);

        if (lot == null || lot.IsDeleted)
            return null;
        
        if (lotUpdateDto.Name != null)
            lot.Name = lotUpdateDto.Name;

        if (lotUpdateDto.Description != null)
            lot.Description = lotUpdateDto.Description;

        if (lotUpdateDto.MinPrice.HasValue)
            lot.MinPrice = lotUpdateDto.MinPrice.Value;

        if (lotUpdateDto.MinStep.HasValue)
            lot.MinStep = lotUpdateDto.MinStep.Value;

        if (lotUpdateDto.IsFinished.HasValue)
            lot.IsFinished = lotUpdateDto.IsFinished.Value;

        await _lotRepository.UpdateAsync(lot);

        return new LotResponseDto
        (
            Id: lot.Id,
            UserId: lot.UserId,
            Name: lot.Name,
            Description: lot.Description,
            MinPrice: lot.MinPrice,
            MinStep: lot.MinStep,
            CurrentPrice: lot.CurrentPrice,
            IsDeleted: lot.IsDeleted,
            IsFinished: lot.IsFinished
        );
    }

    public async Task<bool> DeleteLot(Guid lotId)
    {
        var lot = await _lotRepository.GetByIdAsync(lotId);
        if(lot == null)
            return false;
        
        lot.IsDeleted = true;
        await _lotRepository.UpdateAsync(lot);
        
        return true;
    }
}