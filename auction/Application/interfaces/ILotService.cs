using Application.Dtos;

namespace Application.interfaces;

public interface ILotService
{
    Task<LotResponseDto> AddLot(LotRequestDto dto);
    Task<LotResponseDto?> GetLotById(Guid lotId);
    Task<LotResponseDto?> UpdateLot(Guid lotId, LotUpdateDto dto);
    Task<bool> DeleteLot(Guid lotId);
}