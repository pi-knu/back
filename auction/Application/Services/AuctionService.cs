using Application.Dtos;
using Application.interfaces;
using Domain.Entities;
using Infrastructure.Interfaces;

namespace Application.Services;

public class AuctionService : IAuctionService
{
    private readonly IAuctionRepository _auctionRepository;
    private readonly IBidRepository _bidRepository;

    public AuctionService(
        IAuctionRepository auctionRepository,
        IBidRepository bidRepository)
    {
        _auctionRepository = auctionRepository;
        _bidRepository = bidRepository;
    }

    public async Task<AuctionResponseDto> CreateAuction(AuctionRequestDto dto)
    {
        var auction = new Auction
        {
            Id = Guid.NewGuid(),
            LotId = dto.LotId,
            MinPrice = dto.MinPrice,
            MinSteps = dto.MinSteps,
            CurrentPrice = dto.MinPrice,
            StartDate = DateTime.UtcNow,
            EndDate = dto.EndDate,
            Status = AuctionStatus.Draft,
            UserWinnerId = Guid.Empty
        };

        await _auctionRepository.AddAsync(auction);
        await _auctionRepository.SaveChangesAsync();

        return ToResponse(auction);
    }

    public async Task<AuctionResponseDto?> GetAuction(Guid auctionId)
    {
        var auction = await _auctionRepository.GetByIdAsync(auctionId);
        if (auction == null) return null;

        return ToResponse(auction);
    }

    public async Task<AuctionResponseDto?> UpdateAuction(Guid auctionId, AuctionUpdateDto dto)
    {
        var auction = await _auctionRepository.GetByIdAsync(auctionId);
        if (auction == null) return null;

        if (dto.MinPrice.HasValue)
            auction.MinPrice = dto.MinPrice.Value;

        if (dto.MinSteps.HasValue)
            auction.MinSteps = dto.MinSteps.Value;

        if (dto.EndDate.HasValue)
            auction.EndDate = dto.EndDate.Value;

        if (dto.Status.HasValue)
            auction.Status = dto.Status.Value;

        await _auctionRepository.UpdateAsync(auction);
        await _auctionRepository.SaveChangesAsync();

        return ToResponse(auction);
    }

    public async Task<AuctionResponseDto?> StartAuction(Guid auctionId)
    {
        var auction = await _auctionRepository.GetByIdAsync(auctionId);
        if (auction == null) return null;

        auction.Status = AuctionStatus.Active;
        auction.StartDate = DateTime.UtcNow;

        await _auctionRepository.UpdateAsync(auction);
        await _auctionRepository.SaveChangesAsync();

        return ToResponse(auction);
    }

    public async Task<AuctionResponseDto?> FinishAuction(Guid auctionId)
    {
        var auction = await _auctionRepository.GetByIdAsync(auctionId);
        if (auction == null) return null;

        var bids = await _bidRepository.GetLast10BidsAsync(auctionId);

        if (bids.Count == 0)
        {
            auction.UserWinnerId = Guid.Empty;
        }
        else
        {
            var winnerBid = bids.OrderByDescending(b => b.Price).First();
            auction.UserWinnerId = winnerBid.UserId;
        }

        auction.Status = AuctionStatus.Finished;

        await _auctionRepository.UpdateAsync(auction);
        await _auctionRepository.SaveChangesAsync();

        return ToResponse(auction);
    }

    private AuctionResponseDto ToResponse(Auction auction)
    {
        return new AuctionResponseDto(
            auction.Id,
            auction.LotId,
            auction.MinPrice,
            auction.MinSteps,
            auction.CurrentPrice,
            auction.StartDate,
            auction.EndDate,
            auction.UserWinnerId,
            auction.Status
        );
    }
}
