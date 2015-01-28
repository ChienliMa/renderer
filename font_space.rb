"""
This file will help you crawl fronts from 'www.fontspace.com'
Remember to delete low-quality fonts before using them.
"""
require 'httparty'
require 'nokogiri'
require 'open-uri'
require 'thread'


download_fonts_from 'typewriter', './zips/'


def download_fonts_from cata, output, n_threads = 10
    """
    Down truetype font from Fontspace URL. From page 1 to page n.
    In fact this is more like a rake than normal ruby script.
    -------------------------   
    Parameters:
    	url - fontspace url, such
    	output - output folder where zip file will be saved
    -------------------------
    Returns:
    	None
    """
    n_pages = get_n_pages cata
    p "Totally #{n_pages} pages"

    workers = (0...n_threads).map do
        Thread.new do
            begin
                while n_pages > 0
                    page_index = n_pages
                    n_pages -= 1
                    files_in_page(cata, page_index).each do | pair |
                        # need to print to the screen immediately
                        STDERR.puts "Start downloading '#{pair[:name]}'" + 
                                " from page #{page_index}"
                        download pair
                    end
                end 
            rescue => e
                p e
            end
        end
    end

    workers.map(&:join)
end

def get_n_pages cata
    """
    Get max page num of given catagory
    -----------------
    Parameters:
        cata - String, font style
    -----------------
    Returns:
        num_of_pages, integer
    """
    # open website
    url = "http://www.fontspace.com/category/#{cata}"
    page = Nokogiri::HTML(open(url))
    # get_max_page_num
    page_bar = page.search("//div[@id='content']").search("div[@style=\
                'text-align: right;']")
    n_pages = 0
    page_bar.search("a").each do |a|
        n_pages = n_pages > a.text.to_i ? n_pages : a.text.to_i
    end
    return n_pages  
end

def files_in_page cata, page_index
    """
    Parse certain page of one category to get all the guids and names of 
    all downloadable font files.
    ------------------------------
    Parameters:
        cate - String, catagory of font style
        page_index - Integer, page_index
    ------------------------------
    Returns:
        pairs - List of Hashes. [ { guid: ***, name: *** }, ... ]
    """
    page_url = "http://www.fontspace.com/category/#{cata}?p=#{page_index}"
    page = Nokogiri::HTML(open(page_url))

    pairs = []
    page.search("a[@class='box-button transparent']").each do |a|
        uri = a.attribute('href').value.to_s
        pair = {}
        pair[:guid] = uri.split('/')[-2]
        pair[:name] = uri.split('/')[-1]
        pairs << pair
    end  
    return pairs
end

def download pair, out = './zips/'
    """
    Downlaod fontfile to output path
    ----------------------------
    Parameters:
        pair - Hash, with two key; guid and name of the file
        out - output path
    ----------------------------
    Return:
        Boolean indicating whether download success or not
    """
    download_url = 
        "http://dl1.fontflood.com/download.ashx?guid=#{pair[:guid]}" + \
        "&name=#{pair[:name]}"
    begin
        open( out + pair[:name] , 'wb') do |fo|
            fo.print open(download_url).read
        end
        return true
    rescue => e
        p e
        return false
    end
end

