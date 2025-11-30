using Application.Dtos;

namespace Application.interfaces;

public interface ILotService
{
    Task<LotResponseDto> AddLot(LotRequestDto lotRequestDto);
    Task<LotResponseDto?> GetLotById(Guid lotId);
    Task<LotResponseDto?> UpdateLot(Guid lotId, LotUpdateDto lotUpdateDto);
    Task<bool> DeleteLot(Guid lotId);
}