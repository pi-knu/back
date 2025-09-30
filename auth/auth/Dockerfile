FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 5010

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["./auth.csproj", "auth/"]   
WORKDIR /src/auth
RUN dotnet restore "auth.csproj"
COPY . ./                      
RUN dotnet publish "auth.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "auth.dll"]
