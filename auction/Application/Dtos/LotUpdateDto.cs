namespace Application.Dtos;

public record LotUpdateDto
    (
        string? Name,
        string? Description,
        bool? IsActive
    );