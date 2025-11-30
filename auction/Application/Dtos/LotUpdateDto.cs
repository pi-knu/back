namespace Application.Dtos;

public record LotUpdateDto
    (
        string? Name,
        string? Description,
        decimal? MinPrice,
        int? MinStep,
        bool? IsFinished
    );