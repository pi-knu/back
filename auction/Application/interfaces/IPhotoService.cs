using Application.Dtos;

namespace Application.interfaces;

public interface IPhotoService
{
    Task AddPhoto(PhotoRequestDto dto);
    Task DeletePhoto(Guid lotId, string url);
}