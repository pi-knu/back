namespace Application.Dtos;

public record LotInfoDto
    (
        LotResponseDto Lot,
        List<BidDto> LastBds,
        List<PhotoDto> Photos
    );