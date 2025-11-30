using Application.Dtos;
using Application.interfaces;
using Domain.Entities;
using Infrastructure.Interfaces;

namespace Application.Services;

public class PhotoService : IPhotoService
{
    private readonly IPhotoRepository _photoRepository;

    public PhotoService(IPhotoRepository photoRepository)
    {
        _photoRepository = photoRepository;
    }

    public async Task AddPhoto(PhotoRequestDto dto)
    {
        var photo = new Photo
        {
            Id = Guid.NewGuid(),
            LotId = dto.LotId,
            Url = dto.Url,
            Order = dto.Order
        };

        await _photoRepository.AddAsync(photo);
        await _photoRepository.SaveChangesAsync();
    }

    public async Task DeletePhoto(Guid lotId, string url)
    {
        await _photoRepository.DeleteAsync(lotId, url);
        await _photoRepository.SaveChangesAsync();
    }
}
