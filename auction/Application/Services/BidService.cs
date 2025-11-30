using Application.Dtos;
using Application.interfaces;
using Domain.Entities;
using Infrastructure.Interfaces;

namespace Application.Services;

public class BidService : IBidService
{
    private readonly IBidRepository _bidRepository;

    public BidService(IBidRepository bidRepository)
    {
        _bidRepository = bidRepository;
    }

    public async Task<bool> AddBid(BidDto request)
    {
        var bid = new Bid
        {
            Id = Guid.NewGuid(),
            AuctionId = request.AuctionId,
            UserId = request.UserId,
            Price = request.Price,
            CreatedAt = DateTime.UtcNow,
            IsAborted = false
        };

        await _bidRepository.AddAsync(bid);
        await _bidRepository.SaveChangesAsync();

        return true;
    }
}