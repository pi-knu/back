namespace Application.Dtos;

public record LotRequestDto
    (
        Guid UserId,
        string Name,
        string Description
    );