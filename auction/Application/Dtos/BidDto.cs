namespace Application.Dtos;

public record BidDto
    (
        Guid AuctionId,
        Guid UserId,
        decimal Price
    );