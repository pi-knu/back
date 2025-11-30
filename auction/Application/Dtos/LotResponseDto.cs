namespace Application.Dtos;

public record LotResponseDto
    (
        Guid Id,
        Guid UserId,
        string Name,
        string Description,
        bool IsDeleted,
        bool? IsActive
    );