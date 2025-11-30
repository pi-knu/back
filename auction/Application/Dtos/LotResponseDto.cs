namespace Application.Dtos;

public record LotResponseDto
    (
        Guid Id,
        Guid UserId,
        string Name,
        string Description,
        decimal MinPrice,
        int MinStep,
        decimal CurrentPrice,
        bool IsDeleted,
        bool IsFinished
    );