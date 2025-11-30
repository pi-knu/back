namespace Domain.Entities;

public class Photo
{
    public Guid Id { get; set; }
    public Guid LotId { get; set; }
    public string Url { get; set; } = null;
    public int Order { get; set; }
}