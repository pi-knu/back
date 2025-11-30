using Application.Dtos;

namespace Application.interfaces;

public interface IBidService
{
    Task<bool> AddBid(BidDto request);
}