namespace Domain.Entities;

public class Auction
{
    public Guid Id { get; set; }
    public Guid LotId { get; set; }
    public decimal MinPrice { get; set; }
    public int MinSteps { get; set; }
    public decimal CurrentPrice { get; set; }
    public DateTime StartDate { get; set; }
    public DateTime EndDate { get; set; }
    public Guid UserWinnerId { get; set; }
    public AuctionStatus Status { get; set; }
}

public enum AuctionStatus
{
    Draft, Scheduled, Active, Finished, Cancelled
}