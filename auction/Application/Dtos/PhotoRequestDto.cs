namespace Application.Dtos;

public record PhotoRequestDto
    (
        Guid LotId,
        string Url,
        int Order
    );