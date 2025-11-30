namespace Domain.Entities;

public class Bid
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public Guid AuctionId { get; set; }
    public decimal Price { get; set; }
    public DateTime CreatedAt { get; set; }
    public bool IsAborted { get; set; }
}