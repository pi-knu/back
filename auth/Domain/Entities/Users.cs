namespace Domain.Entities;
using System.ComponentModel.DataAnnotations.Schema;

[Table("users", Schema = "public")]
public class Users
{
    [Column("id")]
    public Guid Id { get; set; }

    [Column("email")]
    public string Email { get; set; }

    [Column("password")]
    public string Password { get; set; }
    
    [Column("created_at")]
    public DateTime CreatedAt { get; set; }
}