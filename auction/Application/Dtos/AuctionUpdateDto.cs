using Domain.Entities;

namespace Application.Dtos;

public record AuctionUpdateDto
    (
        decimal? MinPrice,
        int? MinSteps,
        DateTime? EndDate,
        AuctionStatus? Status
    );