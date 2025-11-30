namespace Domain.Entities;

public class Lot
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public decimal MinPrice { get; set; }
    public int MinStep { get; set; }
    public decimal CurrentPrice { get; set; }
    public bool IsDeleted { get; set; }
    public bool IsFinished { get; set; }
}
