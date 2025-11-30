namespace Application.Dtos;

public record BidDto
    (
        Guid UserId,
        Guid LotId,
        decimal Price,
        DateTime CreatedAt
    );