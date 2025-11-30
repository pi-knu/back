namespace Application.Dtos;

public record AuctionRequestDto
    (
        Guid LotId,
        decimal MinPrice,
        int MinSteps,
        DateTime EndDate
    );