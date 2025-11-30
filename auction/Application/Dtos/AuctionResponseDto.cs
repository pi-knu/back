using Domain.Entities;

namespace Application.Dtos;

public record AuctionResponseDto
    (
        Guid Id,
        Guid LotId,
        decimal MinPrice,
        int MinSteps,
        decimal CurrentPrice,
        DateTime StartDate,
        DateTime EndDate,
        Guid UserWinnerId,
        AuctionStatus Status
    );