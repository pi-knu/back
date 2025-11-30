namespace Domain.Entities;

public class Bid
{
    public Guid UserId { get; set; }
    public Guid LotId { get; set; }
    public decimal Price { get; set; }
    public DateTime Createdat { get; set; }
}